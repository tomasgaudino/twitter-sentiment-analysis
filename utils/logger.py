import logging
import os

# Set up a logger with a file handler and a console handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler to save the log messages to a file in the logs directory
if not os.path.exists('logs'):
    os.makedirs('logs')
log_file_path = 'logs/exceptions.log'
file_handler = logging.FileHandler(log_file_path, mode='a')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Create a stream handler to print the log messages to the console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
