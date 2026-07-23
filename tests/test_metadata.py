from app.database import Base

print("=" * 60)
print("Registered Tables")
print("=" * 60)

for table in Base.metadata.tables:
    print(table)