from flask import Blueprint, request, jsonify
from bson import ObjectId
from services.comment_services import CommentService
from services.user_services import UserService

comment_routes = Blueprint("comment_routes", __name__)

@comment_routes.route("/comments/<post_id>", methods=["GET"])
def get_comments(post_id):
    try:
        response = CommentService.get_post_comments(post_id)
        return jsonify(response), response.get("status", 200)
    except Exception as e:
        return jsonify({"message": str(e), "status": 500}), 500

@comment_routes.route("/comments", methods=["POST"])
def add_comment():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "No token provided", "status": 401}), 401

    try:
        data = request.get_json()
        if not data or not all(k in data for k in ["post_id", "content"]):
            return jsonify({"message": "Missing required fields", "status": 400}), 400

        # Ensure post_id is a valid ObjectId
        try:
            data["post_id"] = ObjectId(str(data["post_id"]))
            if data.get("parent_id"):
                data["parent_id"] = ObjectId(str(data["parent_id"]))
            user_id = ObjectId(UserService.get_user_from_token(token))
        except Exception as e:
            return jsonify({"message": "Invalid ID format", "status": 400}), 400

        response = CommentService.add_comment(data, user_id)
        return jsonify(response), response.get("status", 201)
    except Exception as e:
        return jsonify({"message": str(e), "status": 500}), 500
