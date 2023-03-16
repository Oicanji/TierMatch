from flask import Flask
import os
from flask_login import LoginManager

from .db import db

from .auth import auth
from .views import views

DB_NAME = "notas.db"

__SECRET_KEY = os.getenv("SECRET_KEY")

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = __SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)

    app.register_blueprint(auth, url_prefix='/login')

    app.register_blueprint(views, url_prefix='/')

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    return app
