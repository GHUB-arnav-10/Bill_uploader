import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from app.donut_service import DonutService 


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
   
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    
   
    app.donut_service = DonutService(app.config['DONUT_PRETRAINED_MODEL_NAME'])
    
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


from app import models
