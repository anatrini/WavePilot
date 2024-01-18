import time
import logging

def setup_logger(name, level=logging.INFO, file=False):

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Handler to print on the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(console_handler)

    if file:
        now = time.time()
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime(now))
        file_handler = logging.FileHandler(f'logs/model_info_{timestamp}.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

    return logger