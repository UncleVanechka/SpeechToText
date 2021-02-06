import speech_recognition as sr
import os
import glob

from pydub import AudioSegment
from pydub.silence import split_on_silence
import codecs


def delete_files(path):
    """
    Delete all files from repository
    """
    files = glob.glob(path)
    for f in files:
        os.remove(f)


r = sr.Recognizer()


def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=500,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS - 14,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=600,
                              )
    folder_name = "repository/audio_chunks"
    # create or choose a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, key=None, language='ru-RU')
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    print(whole_text)
    return whole_text


def create_txt_file(content):
    """
        Creating txt file and loading
        all content from audio into it
    """
    folder_name = "repository/text"
    # create or choose a directory to store the audio texts
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    text_file_name = os.path.join(folder_name, f"audio_{content[0:20].split()[0]}.txt")

    fp = codecs.open(text_file_name, "w+", "utf-8-sig")

    try:
        fp.write(content)
    finally:
        fp.close()

