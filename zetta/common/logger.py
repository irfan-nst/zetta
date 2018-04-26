import logging


class Logger:
    class Config:
        output_format = "[%(threadName)s] [%(levelname)s] %(asctime)-15s-%(name)s:%(message)s"
        level = logging.INFO
        app = None

    @classmethod
    def get_logger(cls, name):
        logger = logging.getLogger(name)
        logger.setLevel(cls.Config.level)
        formatter = logging.Formatter(cls.Config.output_format)

        # Console logger
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger
