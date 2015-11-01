__author__ = 'Deepak Verma(verma.dverma.90@gmail.com)'
import logging

from logging import FileHandler, Formatter
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os
import sys


def getPYVERSION():
    vinfo = sys.version_info
    major = vinfo[0]
    minor = vinfo[1]
    micro = vinfo[2]
    return str(major)+'.'+str(minor)+'.'+str(micro)

logging_config = dict(
    version=1,
    formatters={
        'f': {
            'format': '%(filename)s %(asctime)s %(name)-12s %(levelnname)-8s %(message)s'
        }
    },
    handlers={
        'stream_handler':{
            'class':'logging.StreamHandler',
            'formatter': 'f',
            'level': logging.DEBUG
        },
        'file_handler':{
            'class':'logging.FileHandler',
            'formatter': 'f',
            'filename': 'D:/%(name)s.log',
            'level': logging.DEBUG
        },
    },
    loggers={
        'root':{
            'handlers': ['file_handler'],
            'level': logging.DEBUG
        }
    }
)


logger_dict = {}
root_logger_dict = {}
MAX_FILE_SIZE = 1024*1024*512 #512 MB
MAX_FILES = 1024
class LegacyLogger(object):
    def __init__(self, logger_name, fmt=None, log_dir=None, max_file_size=MAX_FILE_SIZE, max_files=MAX_FILES):
        self.logger_name = logger_name
        self.file_count = max_files
        self.max_file_size = max_file_size
        if logger_name in root_logger_dict:
            self.root_logger = root_logger_dict[logger_name]
        else:
            self.root_logger = logging.getLogger(logger_name)
            self.FORMAT = fmt
            self.logdir = log_dir
            if not self.logdir:
                self.logdir = 'D:/'
            if not self.FORMAT:
                self.FORMAT = '%(levelname)s: %(filename)s: %(name)s: %(asctime)-15s: %(lineno)s:  %(message)s'
            self.setConfig()
        root_logger_dict.update({logger_name:self.root_logger})

    def __new__(cls, logger_name,  *args, **kwargs):
        logme = logger_dict.get(logger_name)
        if not logme:
            if getPYVERSION() >= '2.7':
                ins = super(LegacyLogger, cls).__new__(cls)
            else:
                ins = object.__new__(cls, logger_name, *args, **kwargs)
            logger_dict[logger_name] = ins
            return ins
        else:
            return logme

    def setConfig(self):
        self.LOG_FILENAME = os.path.join(self.logdir, self.logger_name+'.log')
        hdlr = self.getHandler()
        fmtr = Formatter(self.FORMAT)
        hdlr.setFormatter(fmtr)
        self.root_logger.addHandler(hdlr)
        self.root_logger.setLevel(logging.DEBUG)

    def getHandler(self):
        #return FileHandler(filename=self.LOG_FILENAME)
        return RotatingFileHandler(filename=self.LOG_FILENAME, maxBytes=self.max_file_size, backupCount=self.max_file_size)

    def setLevel(self, level):
        self.root_logger.setLevel(level)

    def DEBUG(self, message):
        print 'calling'
        self.root_logger.debug(message)

    def INFO(self, message):
        self.root_logger.info(message)

    def WARNING(self, message):
        self.root_logger.warning(message)

    def ERROR(self, message):
        self.root_logger.error(message)

    def CRITICAL(self, message):
        self.root_logger.critical(message)

    def EXCEPTION(self, message):
        self.root_logger.exception(message)


def log_this_message(logger_name, log_level, message, log_dir=None, fmt=None):
    """
    A shorthand function to log your message
    :param logger_name: logger name, this name is also used to create file with this name
    :param log_level: log level like 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'EXCEPTION'
    :param message: Your message
    :param fmt: log record format, according to the logging module specification
    :param log_dir: log folder where log files wil be creating, User of this module/function should make sure s/he has access to this dir
    :return: None
    """
    logger = LegacyLogger(logger_name, fmt, log_dir)
    getattr(logger, log_level.upper())(message)



if __name__=="__main__":
    ags = sys.argv[1:]
    logger_name = ags[0]
    log_level = ags[1]
    message = ags[2]
    log_dir = ags[3]
    log_this_message(logger_name, log_level, message, log_dir)
