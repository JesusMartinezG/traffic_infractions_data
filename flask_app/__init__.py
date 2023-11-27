import os
from flask import Flask
from flask_app.api import api

from flask_app.config import config
from flask_app.database import db

def create_app(run_config='dev'):
    app = Flask(__name__)

    app.config.from_object(config[run_config])

    app.register_blueprint(api.bp)

    db.init_app(app)

    with app.app_context():
      db.create_all()

    return app