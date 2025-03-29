from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.get_database()
user_collection = db["users"]

class User:
    @staticmethod
    def create_user(username, email, password):
        hashed_password = generate_password_hash(password)
        user = {"username": username, "email": email, "password": hashed_password}
        user_collection.insert_one(user)

    @staticmethod
    def find_by_email(email):
        return user_collection.find_one({"email": email})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
