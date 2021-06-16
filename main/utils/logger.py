import logging
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=4)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger = logging.getLogger('request_logger')
logger.addHandler(file_handler)
