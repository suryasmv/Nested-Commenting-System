from flask import Blueprint, request, jsonify
from services.user_services import UserService

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ["username", "email", "password"]):
            return jsonify({"message": "Missing required fields", "status": 400}), 400
        
        response = UserService.signup(data)
        return jsonify(response), response.get("status", 400)
    except Exception as e:
        return jsonify({"message": str(e), "status": 500}), 500

@user_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    response = UserService.login(data)
    return jsonify(response), response.get("status", 400)

@user_routes.route("/logout", methods=["POST"])
def logout():
    try:
        token = request.headers.get("Authorization")
        response = UserService.logout(token)
        return jsonify(response), response.get("status", 400)
    except Exception as e:
        return jsonify({"message": f"Logout failed: {str(e)}", "status": 500}), 500
