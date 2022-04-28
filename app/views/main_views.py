from flask import Flask, render_template, request, Blueprint, current_app
import pickle
import psycopg2
#from logs import log
from riot_api.mongodb import save_log

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['POST', 'GET'])
def index(champ1=None):
    current_app.logger.info("INFO 레벨로 출력")
    return render_template('index.html')

