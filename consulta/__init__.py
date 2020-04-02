# subscription/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_tryton import Tryton
from .utils import get_instance_folder_path
from consulta.config import configure_app
#import logging
#from logging.handlers import RotatingFileHandler
#from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__, instance_path=get_instance_folder_path(),
    instance_relative_config=True)
configure_app(app)
Bootstrap(app)
tryton = Tryton(app)
#app.wsgi_app = ProxyFix(app.wsgi_app)

# register blueprints
from .routes import consulta
app.register_blueprint(consulta)