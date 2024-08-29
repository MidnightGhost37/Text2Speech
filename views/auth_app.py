from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
import datetime

# Function for creating JWT tokens
def create_jwt_token(username):
    expires = datetime.timedelta(days=1)
    return create_access_token(identity=username, expires_delta=expires)
