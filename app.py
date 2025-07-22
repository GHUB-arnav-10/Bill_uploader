import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    
    
    
    
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config_class)

    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    db.init_app(app)
    migrate.init_app(app, db)

    
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


from app import models
