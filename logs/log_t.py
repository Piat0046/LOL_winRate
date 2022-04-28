import logging
import datetime
from config.default import *
from pytz import timezone
from flask import request

logging.basicConfig(filename = f"{BASE_DIR}/logs/cp1.log", level = logging.DEBUG)

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