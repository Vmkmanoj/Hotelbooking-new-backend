# ============================================================
# Standard Library
# ============================================================

# ============================================================
# Third Party
# ============================================================

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.repositories.auth_repositories.auth_repositories import (
    AuthRepository,
)

from app.schema.auth_schema.auth import (
    CustomerRegister,
    PropertyRegister,
    RegisterResponse,
)

from app.schema.auth_schema.login import (
    LoginRequest,
    LoginResponse,
    LoginUser,
)



from app.common.enums.user_enums.role_name import RoleName
from app.common.enums.user_enums.user_status import UserStatus

from app.models.users_models.users import User

from app.core.jwt import create_access_token
from app.core.password import (
    hash_password,
    verify_password,
)


# ============================================================
# Auth Service
# ============================================================

class AuthService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.repo = AuthRepository(db)

    # ========================================================
    # Login
    # ========================================================

    async def login(
        self,
        request: LoginRequest,
    ) -> LoginResponse:

        user = await self.repo.get_user_by_email(
            request.email,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        role = await self.repo.get_user_role(
            user.role_id,
        )


        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": role.name
            }
        )

        await self.repo.update_last_login(
            user,
        )

        return LoginResponse(
            success=True,
            message="Login successful.",
            role=role.name,
            access_token=access_token,
            token_type="Bearer",
            user=LoginUser(
                id=str(user.id),
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                role=role.name,
            ),
        )

    # ========================================================
    # Register Property Owner
    # ========================================================

    async def property_owner_register(
        self,
        request: PropertyRegister,
    ) -> RegisterResponse:

        return await self._register_user(
            request=request,
            role_name=RoleName.PROPERTY_OWNER,
            first_name=request.first_name,
            last_name=request.last_name,
            phone=request.phone,
            avatar_url=request.avatar_url,
        )

    # ========================================================
    # Register Customer
    # ========================================================

    async def customer_register(
        self,
        request: CustomerRegister,
    ) -> RegisterResponse:

        return await self._register_user(
            request=request,
            role_name=RoleName.CUSTOMER,
            first_name=request.userName,
        )

    # ========================================================
    # Common Registration Logic
    # ========================================================

    async def _register_user(
        self,
        request,
        role_name: RoleName,
        first_name: str,
        last_name: str | None = None,
        phone: str | None = None,
        avatar_url: str | None = None,
    ) -> RegisterResponse:

        existing_user = await self.repo.get_user_by_email(
            request.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

        role = await self.repo.get_role_by_name(
            role_name,
        )

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{role_name} role not found.",
            )

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=request.email,
            phone=phone,
            avatar_url=avatar_url,
            password_hash=hash_password(
                request.password,
            ),
            role_id=role.id,
            user_status=UserStatus.ACTIVE,
            created_by=request.email,
            updated_by=request.email,
        )

        await self.repo.create_user(
            user,
        )

        return RegisterResponse(
            success=True,
            message=f"{role_name.value.replace('_', ' ').title()} registered successfully.",
        )