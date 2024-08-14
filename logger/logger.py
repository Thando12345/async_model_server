import logging

def setup_logger():
    """
    Sets up a logger for the application.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.INFO)
    
    # Console handler for terminal output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # File handler for logging to file
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(console_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
