from uuid import uuid4

from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)

user_id = uuid4()

access_token = create_access_token(
    user_id=user_id,
    role="Customer",
)

refresh_token = create_refresh_token(
    user_id=user_id,
)

print("=" * 60)
print("ACCESS TOKEN")
print("=" * 60)
print(access_token)

print()

print("=" * 60)
print("DECODED ACCESS TOKEN")
print("=" * 60)
print(decode_token(access_token))

print()

print("=" * 60)
print("REFRESH TOKEN")
print("=" * 60)
print(refresh_token)

print()

print("=" * 60)
print("DECODED REFRESH TOKEN")
print("=" * 60)
print(decode_token(refresh_token))