import logging
import logging.config


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class LogManager:
    def __init__(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(message)s [%(funcName)s in %(pathname)s]',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.handlers.TimedRotatingFileHandler(
                    'log/debug.log',
                    when='D',
                    interval=1,
                    backupCount=30
                )]
            )
        self.logger = logging.getLogger(__name__)


logger = LogManager().logger
