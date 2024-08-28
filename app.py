from flask import Flask, render_template, Blueprint
from dotenv import load_dotenv
from views.routes import main
from views.db_application import db_app, init_db, create_user, reset_password
import os

app = Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
db_app.init_app(app)
init_db(app)

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000, threaded=True)
