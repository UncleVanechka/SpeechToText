import os


class Config:
    SETUP_CFG = os.path.join(os.path.dirname(__file__), 'setup.cfg')
    REPO_URL = os.getenv('REPO_URL', os.path.join(os.path.dirname(__file__), 'repository/audio_chunks'))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(os.path.dirname(__file__), 'repository/mp3'))
    ALLOWED_EXTENSIONS = {'mp3', 'wav'}
    MP3_PATH = 'repository/mp3/'
    ROOT_NAME = 'repository'
    MP3_NAME = 'repository/mp3'
