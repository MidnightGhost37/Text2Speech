from flask import Blueprint, render_template, request, make_response, send_file, redirect
from werkzeug.utils import secure_filename
from werkzeug.wrappers.response import Response
from utils import tools
import pyttsx3, os, string
from time import sleep


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

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
        return render_template('index.html', filename=filename)
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
