import os
import glob

from flask import Flask, render_template, request, redirect
from pydub import AudioSegment
from werkzeug.utils import secure_filename
from flask import send_file

from model import get_large_audio_transcription, delete_files, create_txt_file
from config import Config

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
app.app_context().push()

@app.route('/download')
def download():
    txts = glob.glob('repository/text/*.txt')
    for txt in txts:
        return send_file(txt,as_attachment=True)


@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:  # no file uploaded
            print("Не могу найти файл")
            return redirect(request.url)  # redirect the user to the home page

        file = request.files["file"]  # if file exist, give that file
        file_ext = file.filename.split(".")[-1]

        if file.filename == "":  # if file is empty, return to the main page
            print("Загруженный файл пустой")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))

        if file:
            delete_files('repository/text/*')
            print("Ваш файл успешно загружен !")

            if file_ext == "mp3":
                abs_path = Config.MP3_PATH + file.filename
                path_mp3file = os.path.abspath(abs_path)
                audio = AudioSegment.from_mp3(path_mp3file)
                audio.export("temp", format="wav")
                file = "temp"

            else:
                raise Exception("Неверный формат файла")

            transcript = get_large_audio_transcription(file)
            delete_files('repository/audio_chunks/*')
            create_txt_file(transcript)
            delete_files('repository/mp3/*')

    return render_template('index.html', transcript=transcript)
