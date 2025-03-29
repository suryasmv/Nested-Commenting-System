from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from bson.json_util import dumps, loads
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.get_database()
comment_collection = db["comments"]

class Comment:
    @staticmethod
    def create_comment(post_id, user_id, content, parent_id=None):
        # Insert new comment document
        comment = {
            "post_id": ObjectId(str(post_id)),
            "user_id": ObjectId(str(user_id)),
            "content": content,
            "parent_id": ObjectId(str(parent_id)) if parent_id else None,
            "created_at": datetime.utcnow()
        }
        result = comment_collection.insert_one(comment)
        return str(result.inserted_id)

    @staticmethod
    def get_comments_by_post(post_id):
        # Fetch and format all comments for a post
        try:
            post_id = ObjectId(str(post_id))
        except:
            raise ValueError("Invalid post ID format")
            
        # MongoDB aggregation pipeline for comments with user data
        pipeline = [
            {"$match": {"post_id": post_id}},
            # Join with users collection to get username
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {"$unwind": "$user"},
            # Format fields for frontend consumption
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "content": 1,
                    "parent_id": {"$toString": "$parent_id"},
                    "created_at": {
                        "$dateToString": {
                            "format": "%Y-%m-%d %H:%M:%S",
                            "date": "$created_at"
                        }
                    },
                    "user_id": {"$toString": "$user_id"},
                    "username": "$user.username",
                    "user_email": "$user.email"
                }
            },
            {"$sort": {"created_at": -1}}  # Newest first
        ]
        return loads(dumps(list(comment_collection.aggregate(pipeline))))

    @staticmethod
    def get_replies(comment_id):
        return list(comment_collection.find({"parent_id": comment_id}))
