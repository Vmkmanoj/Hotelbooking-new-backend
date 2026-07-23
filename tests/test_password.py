from app.core.password import (
    hash_password,
    verify_password,
)

password = "Hello@123"

hashed = hash_password(password)

print(f"Original : {password}")
print(f"Hashed   : {hashed}")

print()

print("Verification")

print(
    verify_password(
        password,
        hashed,
    )
)