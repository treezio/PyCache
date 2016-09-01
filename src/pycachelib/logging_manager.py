'''
   PyCache Sanitize Module

   This module initializes the logging process.

   Configuration is done from a logging.ini file stored in the project
   home directory.

   Usage:

       from pycachelib.logging import logging_manager

       logging_manager.init_logger()
       logger = logging_manager.get_logger()
       logger.level('message')

    @author: Luis Fernandez Tricio
'''

import os
import logging.config
_options = {}


class LoggingInitialisationError(Exception):
    '''Error initializing the logging system.
       @type Exception: exception
       @param Exception: Exception.
    '''
    pass


def init_logger(file_name=None):
    '''
        Logger initialization.

        Logging configuration and initialization using the configuration specified in the file logging.ini
        that must be present in the current working directory.

        @type  file_name: text
        @param file_name: Name of the log file (the extension .log will beappended) and it will be generated
               in the logs directory within the project folder. If set, it overrides the file configured in the logging.ini file.
               Default value: None --> The file name is taken from  the logging.ini.
        @raise LoggerInitialisationError If an error arise when trying to read the logging.ini file or initializing the logger.
    '''
    try:
        cwd = os.getcwd()
        log_ini_path = os.path.join(cwd, 'logging.ini')
        if file_name is not None:
            file_path = os.path.join(cwd, 'logs', file_name + '.log')
            _options['log_file_path'] = file_path
        logging.config.fileConfig(log_ini_path, defaults=_options)
        get_logger().debug('Logging initialized OK')
    except Exception as e:
        raise LoggingInitialisationError(e)


def get_logger(logger_name=''):
    """
    Gets the logger by name.

       Searchs the logger from logging system for the specified name.

       @type  logger_name: text
       @param logger_name: The logger name to be retrieved. Default is \'\'
                           and corresponds to root logger.
       @rtype: instance
       @return: C{logger} A logger instance with name `logger_name`
    """
    return logging.getLogger(logger_name)
