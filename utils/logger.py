import logging
import os
from datetime import datetime


class LogGenerator:

    @staticmethod
    def loggen():

        # Create logs directory
        log_dir = "logs"

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Dynamic log file
        log_file = os.path.join(
            log_dir,
            f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        # Create custom logger
        logger = logging.getLogger("automation_logger")

        logger.setLevel(logging.INFO)

        # Prevent duplicate logs
        if logger.hasHandlers():
            logger.handlers.clear()

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # File Handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger