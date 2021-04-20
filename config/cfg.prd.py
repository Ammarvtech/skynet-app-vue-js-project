import os
import logging
from logging.handlers import TimedRotatingFileHandler

################ Create needed path's ####################
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(CURRENT_PATH, os.pardir))
LOGGING_PATH = os.path.abspath(os.path.join(CURRENT_PATH, os.pardir, 'logs'))
CACHE_PATH = os.path.join(CURRENT_PATH + '/cache')
##########################################################

SERV_IP = '0.0.0.0'
SERV_PORT = 8888
SERV_MODE = 'gevent'


DEALER_HOST = 'ec2-54-172-51-46.compute-1.amazonaws.com'
# 'session.timeout': 3600 * 24,  # 1 day

SESSION_OPT = {
    'session.cookie_expires': True,
    'session.encrypt_key': '24',
    'session.secure': False,
    'session.httponly': True,
    'session.timeout': 3600*24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}

AWS_SMTP = {
    'Username': 'AKIAIDWHWPLZLJHEROPA',
    'Password': 'BAiCDbBasuYMHrOUm33jCisKlVBrog0VP2/iyN4HVg19',
    'Server': 'email-smtp.us-east-1.amazonaws.com'
}

SQS_REGION = 'us-east-1'
SQS_ACCESS_KEY = 'AKIAIQVENYOUZY36IT4Q'
SQS_SECRET_KEY = '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'
SQS_ALERT_QUEUE_NAME = 'dev-dlr-alerts.fifo'

DB_SETTINGS = {
    'user': 'snh_remote_user',
    'password': 'musAncheLL0_GomeZ!',
    'db': 'skynet_harvester',
    'host': 'db-prd.skyneto.com',
    'port': 3306
}


DB_TEST = "SELECT * FROM  `skynet_dash`.`campaigns_final_data` WHERE data_date='2017-11-13'"


formatter = logging.Formatter(fmt='[%(asctime)s.%(msecs)d] [%(name)s] [%(levelname)s] %(message)s', datefmt='%H:%M:%S')


def set_logger(name, log_file_name, level=logging.INFO):
    """Function setup as many loggers as you want"""
    handler = TimedRotatingFileHandler(LOGGING_PATH + '/' + log_file_name, "midnight", 1, 14)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
