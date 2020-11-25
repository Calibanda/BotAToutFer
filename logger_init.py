import os
import logging

import const

def logger_init():
    if not os.path.exists(const.LOG_DIR): # If the logs directory does not exist, we create it
        os.makedirs(const.LOG_DIR)

    # Setting up the logging system
    logger = logging.getLogger("discord")
    logger.setLevel(logging.WARNING)
    handler = logging.FileHandler(filename=const.LOG_FILE_PATH, encoding="utf-8", mode="a")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)

    return logger
