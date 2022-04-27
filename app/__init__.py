from flask import Flask, render_template, request
import pickle
import psycopg2



def create_app():

    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')
    
    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app