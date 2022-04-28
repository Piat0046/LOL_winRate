from flask import Flask, render_template #request
import pickle
import psycopg2
from config.default import *
from logs import log


def create_app():
    
    app = Flask(__name__)
    #app.config.from_envvar('APP_CONFIG_FILE')
    #log.log(request, "hello route")
    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app