import logging
import datetime
from config.default import *
from pytz import timezone
from flask import request

logging.basicConfig(filename = f"{BASE_DIR}/logs/cp1.log", level = logging.DEBUG)

import logging
from logging.handlers import RotatingFileHandler  
# logging 핸들러에서 사용할 핸들러를 불러온다.
file_handler = RotatingFileHandler(
    'dave_server.log', maxBytes=2000, backupCount=10)
file_handler.setLevel(logging.WARNING)  
# 어느 단계까지 로깅을 할지를 적어줌
# app.logger.addHandler() 에 등록시켜줘야 app.logger 로 사용 가능
#app.logger.addHandler(file_handler)


def log(request, message):
    log_date = get_log_date()
    log_message = "{0}/{1}/{2}".format(log_date, str(request), message)
    logging.info(log_message)

def error_log(request, error_code, error_message):
    log_date = get_log_date()
    log_message = "{0}/{1}/{2}/{3}".format(log_date, str(request), error_code, error_message)
    logging.info(log_message)

def get_log_date():
    dt = datetime.datetime.now(timezone("Asia/Seoul"))
    log_date = dt.strftime("%Y%m%d_%H:%M:%S")
    return log_date