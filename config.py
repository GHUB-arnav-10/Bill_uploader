import os
from dotenv import load_dotenv


load_dotenv()


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a-very-secret-key')
    FLASK_APP = os.environ.get('FLASK_APP', 'app.py')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 1)

    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    
    
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    
    
    
    DONUT_PRETRAINED_MODEL_NAME = os.environ.get('DONUT_PRETRAINED_MODEL_NAME', 'naver-clova-ix/donut-base-finetuned-cord-v2')
    
    DONUT_TASK_PROMPT = "<s_cord-v2>"

    
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
