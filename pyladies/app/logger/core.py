import logging
import logging.config


class LogManager:
    def __init__(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M',
            handlers=[logging.handlers.TimedRotatingFileHandler('log/debug.log',when='D',interval=1,backupCount=30)])
        self.logger = logging.getLogger()

logger = LogManager().logger