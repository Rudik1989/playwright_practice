from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from os import path, makedirs

import allure


class AllureHandler(StreamHandler):

    def emit(self, record):
        try:
            with allure.step(str(record.msg)):
                pass
        except KeyError:
            pass


class TestDependentRotatingFileHandler(RotatingFileHandler):
    log_filename = None

    def __init__(self):
        # We need to path here empty string as we don't care about this param
        # also we cant pass here None because some errors on Linux
        super(TestDependentRotatingFileHandler, self).__init__('')

    def _open(self):
        stream = None
        log_filename = TestDependentRotatingFileHandler.log_filename
        if log_filename:
            log_folder = path.dirname(log_filename)

            if not path.isdir(log_folder):
                makedirs(log_folder)

            stream = open(log_filename, self.mode)
        return stream

    def emit(self, record):
        if not TestDependentRotatingFileHandler.log_filename:
            return
        self.stream = None
        super(TestDependentRotatingFileHandler, self).emit(record)
