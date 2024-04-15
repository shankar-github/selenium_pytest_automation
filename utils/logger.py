# utils/logger.py
import logging
from datetime import datetime


def get_logger(name):
    # Get current date and time
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"test_{current_time}.log"  # Append current time to file name

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set the level to DEBUG
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and set the format for the logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger
