from flask import Flask, render_template, Blueprint
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from dotenv import load_dotenv
from views.routes import main
from views.db_application import db_app, init_db, create_user, reset_password, get_user, encrypt_password
import os

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.urandom(16).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['JWT_SECRET_KEY'] = os.urandom(16).hex()
app.config['JWT_TOKEN_LOCATION'] = ['cookies']    # Store JWT in cookies
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

db_app.init_app(app)
init_db(app)

jwt = JWTManager(app)

app.register_blueprint(main)

@jwt.invalid_token_loader
def handle_jwt_errors(e):
    return render_template('error.html', error_name="Invalid JWT provided!")

@app.errorhandler(404)
def handle_exception(e):
    return render_template("error.html", error_name=e.name), e.code

@app.errorhandler(NoAuthorizationError)
def handle_no_authorization_error(e):
    return render_template('error.html', error_name="No Authorization header provided!")

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000, threaded=True)
