from os import path
import logging
import logging.config


main_logger_name = 'shared'
log_config_file = 'logger.json'
log_config_path = path.join(path.dirname(__file__), log_config_file)


def get_logger(name=''):
    log = logging.getLogger(name or main_logger_name)
    return log
