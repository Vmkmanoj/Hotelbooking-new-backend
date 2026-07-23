from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permissions_models.permissions import Permission
from app.models.permissions_models.roles import Role
from app.models.permissions_models.roles_permission import RolePermission


ROLES = [
    ("SUPER_ADMIN", "Platform Owner"),
    ("PROPERTY_OWNER", "Hotel Owner"),
    ("CUSTOMER", "Customer"),
]

PERMISSIONS = [
    ("property.create", "PROPERTY", "Create Property"),
    ("property.update", "PROPERTY", "Update Property"),
    ("property.delete", "PROPERTY", "Delete Property"),
    ("property.view", "PROPERTY", "View Property"),
    ("room.create", "ROOM", "Create Room"),
    ("room.update", "ROOM", "Update Room"),
    ("room.delete", "ROOM", "Delete Room"),
    ("room.view", "ROOM", "View Room"),
    ("booking.create", "BOOKING", "Create Booking"),
    ("booking.view", "BOOKING", "View Booking"),
    ("booking.update", "BOOKING", "Update Booking"),
    ("booking.cancel", "BOOKING", "Cancel Booking"),
    ("booking.checkin", "BOOKING", "Check-In Guest"),
    ("booking.checkout", "BOOKING", "Check-Out Guest"),
    ("payment.view", "PAYMENT", "View Payment"),
    ("payment.refund", "PAYMENT", "Refund Payment"),
    ("review.create", "REVIEW", "Create Review"),
    ("review.delete", "REVIEW", "Delete Review"),
    ("user.create", "USER", "Create User"),
    ("user.update", "USER", "Update User"),
    ("user.delete", "USER", "Delete User"),
    ("user.view", "USER", "View User"),
]

ROLE_PERMISSIONS = {
    "SUPER_ADMIN": None,  # None means every permission.
    "PROPERTY_OWNER": {
        "property.create", "property.update", "property.view",
        "room.create", "room.update", "room.delete", "room.view",
        "booking.view", "booking.checkin", "booking.checkout",
        "payment.view", "review.create",
    },
    "CUSTOMER": {
        "property.view", "room.view", "booking.create", "booking.view",
        "booking.cancel", "payment.view", "review.create",
    },
}


async def seed_database(db: AsyncSession) -> None:
    """Create the default roles, permissions, and role mappings if absent."""
    try:
        existing_roles = {
            role.name: role
            for role in (await db.execute(select(Role))).scalars()
        }
        for name, description in ROLES:
            if name not in existing_roles:
                role = Role(name=name, description=description)
                db.add(role)
                existing_roles[name] = role

        existing_permissions = {
            permission.name: permission
            for permission in (await db.execute(select(Permission))).scalars()
        }
        for name, modules, description in PERMISSIONS:
            if name not in existing_permissions:
                permission = Permission(
                    name=name,
                    modules=modules,
                    description=description,
                )
                db.add(permission)
                existing_permissions[name] = permission

        # Assign IDs to newly-created rows before creating role-permission links.
        await db.flush()

        existing_links = {
            (link.rolesId, link.permission_id)
            for link in (await db.execute(select(RolePermission))).scalars()
        }
        for role_name, permission_names in ROLE_PERMISSIONS.items():
            role = existing_roles[role_name]
            names = existing_permissions.keys() if permission_names is None else permission_names
            for permission_name in names:
                permission = existing_permissions[permission_name]
                link_key = (role.id, permission.id)
                if link_key not in existing_links:
                    db.add(RolePermission(
                        rolesId=role.id,
                        permission_id=permission.id,
                    ))
                    existing_links.add(link_key)

        await db.commit()
    except Exception:
        await db.rollback()
        raise
