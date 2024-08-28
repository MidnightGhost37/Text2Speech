from flask_sqlalchemy import SQLAlchemy
import os
from hashlib import sha256

# Initialize SQLAlchemy
db_app = SQLAlchemy()

# Define the Users table
class User(db_app.Model):
    __tablename__ = 'Users'
    Username = db_app.Column(db_app.String(255), primary_key=True, unique=True, nullable=False)
    Password = db_app.Column(db_app.String(255), nullable=False)
    Email = db_app.Column(db_app.String(255), unique=True, nullable=False)
    ResetToken = db_app.Column(db_app.String(255), nullable=True)


def init_db(app):
    with app.app_context():
        db_app.drop_all()   # Drops all tables if they exist
        db_app.create_all() # Creates the tables


def create_user(username:str, email:str, password:str, sql_alchemy_session)->tuple:
    reset_token = os.urandom(16).hex()

    if ( sql_alchemy_session.query(User).filter(User.Username == username).first()) or ( sql_alchemy_session.query(User).filter(User.Email == email).first()):
        return "Account already exists", None

    password = sha256(password.encode()).hexdigest()
    new_user = User(Username=username, Email=email, Password=password, ResetToken=reset_token)
    sql_alchemy_session.add(new_user)
    sql_alchemy_session.commit()
    return "User registered successfully", reset_token

def reset_password(username:str, new_password:str, reset_token:str, sql_alchemy_session)->str:
    if not ( sql_alchemy_session.query(User).filter(User.ResetToken == reset_token).first()):
        return "Invalid reset token"

    user = sql_alchemy_session.query(User).filter(User.Username == username).first()
    new_password = sha256(new_password.encode()).hexdigest()
    user.Password = new_password
    sql_alchemy_session.commit()
    return "Password reset successfully"
