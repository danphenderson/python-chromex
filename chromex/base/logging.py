# chromex/base/logging.py

import logging

def setup_logger(name='chromex', level=logging.INFO, handler=None):
    """
    Set up a logger for the chromex library.

    This function initializes and configures a logger with a specified name, logging level, and handler. 
    If no handler is provided, a default console handler is created and used.

    The logger is set up to output log messages including the timestamp, logger name, log level, and the log message itself.

    :param name: Name of the logger. Default is 'chromex'.
    :type name: str
    :param level: Logging level, e.g., logging.INFO. Default is logging.INFO.
    :type level: int
    :param handler: Logging handler. If None, defaults to a console handler.
    :type handler: logging.Handler, optional
    :return: Configured logger instance.
    :rtype: logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Create handler if not provided
        if handler is None:
            handler = logging.StreamHandler()

        # Create formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)

    return logger

# You can then create a logger instance for your package
logger = setup_logger()

# Example of how to use it in other modules
# from chromex.base.logging import logger
# logger.info("This is an info message")