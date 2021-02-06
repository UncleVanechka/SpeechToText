import os


class Config:
    SETUP_CFG = os.path.join(os.path.dirname(__file__), 'setup.cfg')
    REPO_URL = os.getenv('REPO_URL', os.path.join(os.path.dirname(__file__), 'audio_chunks'))
