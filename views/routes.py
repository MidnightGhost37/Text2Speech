from flask import Blueprint, render_template, request, make_response, send_file, redirect, jsonify
from werkzeug.utils import secure_filename
from werkzeug.wrappers.response import Response
from utils import tools
import pyttsx3, os, string
from time import sleep
from views.auth_app import create_jwt_token, login_required



main = Blueprint('main', __name__)

@main.route('/sings', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@login_required
@main.route('/', methods=['GET'])
def home():
    if request.cookies.get('JWT'):
        return redirect('/sings')

    return redirect('/login')

@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@main.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    data = request.get_json()
    username, email, password = data['username'], data['email'], data['password']

    from __main__ import db_app, create_user;
    sql_alchemy_session = db_app.session
    object = create_user(username, email, password, sql_alchemy_session);
    message, reset_token = object if type(object) == tuple else (object, None)

    return jsonify({"message": message, "reset_token": reset_token}) if reset_token else jsonify({"message": message})

@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.get_json()
    username, password = data['username'], data['password']

    from __main__ import db_app, get_user, encrypt_password, jwt;
    sql_alchemy_session = db_app.session
    user = get_user(username, sql_alchemy_session)
    if (not user) or (user.Password != encrypt_password(password)):
        return jsonify({"error": "User authentication failed!: Check your username and password"})

    token = create_jwt_token(username)
    return jsonify({"message": "User authenticated successfully!", "token": token})


@main.route('/speech_converter', methods=['POST'])
def speech_converter():
    engine = pyttsx3.init()

    if request.form:
        text = request.form['lyrics']
        if len(list(set(text).intersection(set(string.ascii_letters + string.digits)))) == 0:
            return render_template("error.html", error_name="No text provided")
        try:
            filename = secure_filename(request.form['filename']) if request.form['filename'] else secure_filename(f"{tools.random_string(16)}")
        except:
            filename = secure_filename(f"{tools.random_string(16)}")

        engine.save_to_file(text, f"voices_files/{filename.replace('/', '')}.mp3")
        engine.runAndWait()

        # Redirect to success page
        return render_template('success.html', filename=filename)
    else:
        return render_template("error.html", error_name="No text provided")

@main.route('/voice_files/<filename>', methods=['GET'])
def filename_download(filename: str):
    filename = secure_filename(filename)
    file_path = os.path.join("voices_files", filename)

    if not os.path.exists(file_path):
        return render_template("error.html", error_name="File not found")

    return send_file(file_path, as_attachment=True)

@main.route("/success")
def success(filename:str)->str:
    return render_template('success.html')
