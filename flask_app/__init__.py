import os
from flask import Flask
import locale

from flask_app.config import config
from flask_app.database import db


def create_app(run_config='dev'):
    app = Flask(__name__, static_folder='webapp/static')
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    app.config.from_object(config[run_config])

    from flask_app.api.routes import bp as api_blueprint
    app.register_blueprint(api_blueprint)

    from flask_app.webapp.routes import bp as webapp_bluerint
    app.register_blueprint(webapp_bluerint, url_prefix='/')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app