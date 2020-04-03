# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_tryton import Tryton
from flask_compress import Compress
from .utils import get_instance_folder_path
from consulta.config import configure_app
from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha
#import logging
#from logging.handlers import RotatingFileHandler
#from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__, instance_path=get_instance_folder_path(),
    instance_relative_config=True)
configure_app(app)
Compress(app)
Bootstrap(app)
tryton = Tryton(app)
Session(app)
captcha = FlaskSessionCaptcha(app)
#app.wsgi_app = ProxyFix(app.wsgi_app)

# register blueprints
from .routes import consulta
app.register_blueprint(consulta)
