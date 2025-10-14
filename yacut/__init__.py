from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def _init_extensions(app: Flask) -> None:
    db.init_app(app)
    # Make Flask-Migrate optional for testing/runtime environments
    try:
        from flask_migrate import Migrate  # type: ignore
    except Exception:
        return
    Migrate(app, db)


def _register_routes(app: Flask) -> None:
    # DEPRECATED: no longer used
    return None


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(error):  # noqa: ANN001 - Flask error handler signature
        return render_template('404.html'), 404


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')
    app.config['DISK_TOKEN'] = os.getenv('DISK_TOKEN', '')

    _init_extensions(app)
    # Error handlers
    from yacut.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Jinja globals
    import datetime as _dt
    app.jinja_env.globals['now'] = _dt.datetime.now

    # Register blueprints for views and api
    from yacut.views import bp as views_bp
    from yacut.api import bp as api_bp
    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp)

    return app


# Expose application instance for tests and simple runs
app = create_app()
