import csv
import sys
import logging
from logging import handlers
from database_helper import DatabaseHelper
from config_helper import ConfigHelper


def init_config():
    config = ConfigHelper()
    config.load_config()
    return config


Config = init_config()


def _init_logger(name, log_file):
    logger = logging.getLogger(name)
    handler = logging.handlers.RotatingFileHandler(log_file, 'a', maxBytes=10485760, backupCount=10)
    log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s.%(funcName)s: %(lineno)d] %(message)s')
    handler.setFormatter(log_format)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger


_Logger_container = {}


def get_logger(name):
    global _Logger_container
    if name in _Logger_container:
        return _Logger_container[name]
    
    log_file = Config.log_info_map.get(name)
    _Logger_container[name] = _init_logger(name, log_file)
    return _Logger_container[name]


def get_db_hander(name):
    db = Config.db_info_map.get(name)
    return DatabaseHelper(**db)


def write_csv(file_name, output):
    with open(file_name, 'w', encoding='utf-8-sig') as csv_file:
        printer = csv.writer(csv_file)
        printer.writerow(output)

    
def write_txt(file_name, mode, output):
    with open(file_name, mode, encoding='utf-8-sig') as fin:
        for item in output:
            fin.write(item)
            fin.write("\n")