from flask import Flask, render_template, request, redirect
import speech_recognition as sr
from pydub import AudioSegment
import os

from model import get_large_audio_transcription, delete_files, create_txt_file

app = Flask(__name__, template_folder='templates')
app.app_context().push()


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

        if file:
            delete_files('text/*')
            print("Ваш файл успешно загружен !")
            if file_ext == "mp3":
                path_mp3file = os.path.abspath(file.filename)
                audio = AudioSegment.from_mp3(path_mp3file)
                audio.export("temp", format="wav")
                file = "temp"
            else:
                raise Exception("Неверный формат файла")
            transcript = get_large_audio_transcription(file)
            delete_files('audio_chunks/*')
            create_txt_file(transcript)

    return render_template('index.html', transcript=transcript)
