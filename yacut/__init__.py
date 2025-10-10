from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URI', 'sqlite:///db.sqlite3'
    )
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')
    app.config['DISK_TOKEN'] = os.getenv('DISK_TOKEN', '')

    db.init_app(app)
    migrate.init_app(app, db)

    return app
