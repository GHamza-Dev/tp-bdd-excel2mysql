import logging

def setup_logging(LOGGING_CONFIG):
    # Initialize logger
    logger = logging.getLogger()
    logger.setLevel(LOGGING_CONFIG["log_level"])

    # Create a file handler to log to a file
    file_handler = logging.FileHandler(LOGGING_CONFIG["log_file"])
    file_handler.setLevel(LOGGING_CONFIG["log_level"])

    # Create a stream handler to log to console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOGGING_CONFIG["log_level"])

    # Define the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
