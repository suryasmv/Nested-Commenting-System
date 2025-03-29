import jwt
import datetime
from models.user_models import User
from config import SECRET_KEY

# Store active JWT tokens in memory for blacklisting on logout
active_tokens = set()

# Header: Algorithm HS256 (HMAC with SHA-256)
# Payload: Contains email and expiration time
# Signature: Created using the secret key from secret_key.txt

# Add these constants at the top of the file
JWT_HEADER = {
    "alg": "HS256",
    "typ": "JWT"
}

class UserService:
    @staticmethod
    def signup(data):
        # Validate and create new user account
        try:
            # Check if email is already registered
            if User.find_by_email(data["email"]):
                return {"message": "User already exists", "status": 400}
            
            # Validate password length
            if len(data["password"]) < 6:
                return {"message": "Password must be at least 6 characters", "status": 400}
            
            # Create new user with hashed password
            User.create_user(data["username"], data["email"], data["password"])
            return {"message": "User registered successfully", "status": 201}
        except Exception as e:
            return {"message": f"Error during signup: {str(e)}", "status": 500}

    @staticmethod
    def login(data):
        # Verify credentials and generate JWT token
        user = User.find_by_email(data["email"])
        if not user or not User.verify_password(user["password"], data["password"]):
            return {"message": "Invalid email or password", "status": 401}

        # Generate JWT token with explicit structure
        payload = {
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            "iat": datetime.datetime.utcnow(),  # issued at
            "sub": str(user["_id"])  # subject (user id)
        }

        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm="HS256",
            headers=JWT_HEADER
        )
        active_tokens.add(token)
        return {"message": "Login successful", "token": token, "status": 200}

    @staticmethod
    def logout(token):
        # Remove token from active sessions
        try:
            if not token:
                return {"message": "No token provided", "status": 401}

            # Extract token from Bearer header
            if token.startswith('Bearer '):
                token = token.split(' ')[1]

            # Validate token before blacklisting
            try:
                jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            except jwt.InvalidTokenError:
                return {"message": "Invalid token", "status": 401}
            except jwt.ExpiredSignatureError:
                return {"message": "Token expired", "status": 401}

            # Blacklist token
            if token in active_tokens:
                active_tokens.remove(token)
                return {"message": "Logout successful", "status": 200}
            
            return {"message": "Token not found in active sessions", "status": 401}
        except Exception as e:
            return {"message": f"Error during logout: {str(e)}", "status": 500}

    @staticmethod
    def get_user_from_token(token):
        # Extract user ID from JWT token
        try:
            # Handle Bearer token format
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            
            # Decode and validate token
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = User.find_by_email(payload["email"])
            if not user:
                raise Exception("User not found")
            return str(user["_id"])
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
