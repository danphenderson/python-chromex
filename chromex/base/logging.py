# chromex/base/logging.py

import logging

def setup_logger(name='chromex', level=logging.INFO, handler=None):
    """
    Set up a logger for chromex library.

    Args:
        name (str): Name of the logger.
        level (int): Logging level, e.g., logging.INFO.
        handler (logging.Handler): Logging handler. Defaults to console handler if None.
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