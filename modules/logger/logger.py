import logging
import coloredlogs
import os


class FtLogger:
    def get_logger(name, verbose):
        logger = logging.getLogger(name)
        coloredlogs.DEFAULT_DATE_FORMAT = '%H:%M:%S'
        coloredlogs.DEFAULT_LOG_FORMAT = '[%(levelname)s] %(message)s'
        coloredlogs.DEFAULT_FIELD_STYLES = {'asctime': {'color': 'black', 'bright': True}, 'levelname': {'bold': True, 'color': 'yellow'}}
        coloredlogs.install(level=verbose, logger=logger)
        return logger

