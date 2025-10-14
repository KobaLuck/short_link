from flask import render_template, Blueprint, jsonify


bp_errors = Blueprint('errors', __name__)


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):  # noqa: ANN001 - Flask error handler signature
        # Render HTML for web requests
        return render_template('404.html'), 404

    # You can add more handlers here (e.g., 400/500) if needed


