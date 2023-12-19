import os

from flask import Flask
from flask_cors import CORS


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        COMFY_URL='http://127.0.0.1:3000/',
        CONFIG_BUCKET=os.getenv('CONFIG_BUCKET', 'pumky-config'),
        RULE_FILE=os.getenv('RULE_FILE', 'rule.json')
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import (rule, convert)
    app.register_blueprint(rule.bp)
    app.register_blueprint(convert.bp)

    @app.route('/')
    def index():
        return "Hello Off members!"

    CORS(app)
    return app
