import logging
from logging.handlers import RotatingFileHandler

log = logging.getLogger('SortLog')


def logconfig():
    """
    Конфигурация логгера
    :return:
    """
    LOG_FORMAT = '%(asctime)s : %(levelname)s - %(message)s'
    stream_logger = logging.StreamHandler()
    stream_logger.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    stream_logger.setLevel(logging.DEBUG)
    log.addHandler(stream_logger)
    filehandler = RotatingFileHandler('sms_logger.log', mode='a', maxBytes=10, encoding='utf-8')

    formatter = logging.Formatter(LOG_FORMAT)
    formatter.datefmt = '%d-%m-%Y %H:%M'
    filehandler.setLevel(logging.DEBUG)
    # все возможные аттрибуты см https://docs.python.org/3.5/library/logging.html#logrecord-attributes
    filehandler.setFormatter(formatter)
    log.addHandler(filehandler)
    log.setLevel(logging.DEBUG)
    # logging.basicConfig(handlers=(filehandler, stream_logger))
