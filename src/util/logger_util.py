import logging
import os


def setup_logger(name, level=logging.INFO):
    """
    Setup logging configuration.

    :param name: The name of the logger.
    :param level: The logging level (default is INFO).
    :return: The configured logger.
    """
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(name)

    # Check if logger is already present
    if not logger.handlers:
        # Set up logging for Lambda environment
        if 'LAMBDA_LOG' in os.environ:
            handler = logging.StreamHandler()  # Log to stdout for Lambda
        else:
            handler = logging.FileHandler('app.log')  # Log to file for local environment
        handler.setFormatter(formatter)
        logger.setLevel(level)
        logger.addHandler(handler)

    return logger


def get_logger():
    """
    Get a configured logger.

    :return: The configured logger.
    """
    return setup_logger('app_logger')
