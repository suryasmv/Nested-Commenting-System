from flask import Flask, jsonify
from flask_cors import CORS
from routes.user_routes import user_routes
from routes.comment_routes import comment_routes

app = Flask(__name__)
# Configure CORS with specific settings
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5175"],  # Your React frontend URL
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"message": "Bad request", "status": 400}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Internal server error", "status": 500}), 500

app.register_blueprint(user_routes)
app.register_blueprint(comment_routes)

if __name__ == "__main__":
    app.run(debug=True)
