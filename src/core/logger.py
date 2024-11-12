import logging


class LoggingUtil:
    """
    Util to create logs in console
    """

    @classmethod
    def setup_logger(cls):
        logger = logging.getLogger("telegram-embedding-bot")
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
