import os
import secrets

SECRET_KEY_FILE = "secret_key.txt"
MONGO_URI = "mongodb://localhost:27017/Nested-Commenting-System"

if not os.path.exists(SECRET_KEY_FILE):
    with open(SECRET_KEY_FILE, "w") as f:
        f.write(secrets.token_hex(32))

with open(SECRET_KEY_FILE, "r") as f:
    SECRET_KEY = f.read().strip()
