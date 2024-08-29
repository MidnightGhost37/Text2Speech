from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
import datetime
# Decorator for checking if user is logged in
def login_required(f):
    def checking_jwt(*args, **kwargs):
        from __main__ import jwt;
        try:
            get_jwt_identity()
        except Exception as e:
            return {"error": "User not authenticated!"}
        return f(*args, **kwargs)

    return checking_jwt

# Function for creating JWT tokens
def create_jwt_token(username):
    expires = datetime.timedelta(days=1)
    return create_access_token(identity=username, expires_delta=expires)
