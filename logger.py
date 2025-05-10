import logging
import os
import time

from constants import LOG_FOLDER
from logging.handlers import QueueHandler


def setup_logger(name, log_queue=None, level=logging.INFO, file=False):
    folder_path = LOG_FOLDER

    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder created: {folder_path}")
        else:
            # print(f"Logs folder already exists: {folder_path}")
            pass
    except OSError as e:
        print(f"Error: {e}")

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Config handlers if not already configured
    if not logger.hasHandlers():
        if log_queue:
            queue_handler = QueueHandler(log_queue)
            logger.addHandler(queue_handler)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
            logger.addHandler(console_handler)

        # Add file handler only if required and not already present
        if file and not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
            now = time.time()
            timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime(now))
            file_handler = logging.FileHandler(f"logs/reduction_info_{timestamp}.log")
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            logger.addHandler(file_handler)

    return logger
