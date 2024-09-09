import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lorem-ipsum-dolo'
    # RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    # RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    # RECAPTCHA_PARAMETERS = {'hl':'es'}
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
    PATH_BOLETAS = os.path.join(basedir, 'u', 'boletas')
    IMG_BOLETAS = os.path.join(basedir, 'u', 'boletas', 'pics')
    UPLOAD_PATH_FOTOS = os.path.join(basedir, 'u', 'fotos')
    UPLOAD_PATH_FOTOS_EV = os.path.join(basedir, 'u', 'fotos_ev')
    EXCEL_PATH = os.path.join(basedir, 'excel')
    