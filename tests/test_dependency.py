from app.core.jwt import create_access_token
from app.core.jwt import decode_token

token = create_access_token(
    user_id="123",
    role="CUSTOMER",
)

payload = decode_token(token)

print(payload)