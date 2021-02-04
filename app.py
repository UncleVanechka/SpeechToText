from flask import Flask, render_template, request, redirect
import speech_recognition as sr
from pydub import AudioSegment
import os

app = Flask(__name__, template_folder='templates')
app.app_context().push()


@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        file_ext = file.filename.split(".")[-1]
        if file.filename == "":
            return redirect(request.url)

        if file:
            if file_ext == "mp3":
                path_mp3file = os.path.abspath(file.filename)
                audio = AudioSegment.from_mp3(path_mp3file)
                audio.export("temp", format="wav")
                file = "temp"
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                data = recognizer.record(source)
                print("Working on...")
            try:
                transcript = recognizer.recognize_google(data, key=None, language='ru-RU')
            except:
                print("Sorry... run again...")

    return render_template('index.html', transcript=transcript)
