import os

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI is not set!")

print("✅ MONGO_URI:", MONGO_URI)