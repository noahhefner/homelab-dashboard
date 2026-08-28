import os

from flask import Flask

from app.config import ConfigLoader, DEFAULT_CONFIG_PATH
from app.security import validate_url


def create_app(config_path=None):
    app = Flask(__name__)

    path = config_path or os.environ.get("CONFIG_PATH") or DEFAULT_CONFIG_PATH
    app.config["CONFIG_PATH"] = path
    app.extensions["dashboard_loader"] = ConfigLoader(path)

    app.jinja_env.tests["url"] = validate_url

    from app.views import bp

    app.register_blueprint(bp)

    return app
