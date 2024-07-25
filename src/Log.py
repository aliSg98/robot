import logging

class Log:
    def __init__(self):
        self._logger = logging.getLogger('log')
        self._logger.setLevel(logging.INFO)
        self._handler = logging.FileHandler(r"C:\Users\nasudre\Desktop\Robot\LOG\log.txt")
        self._format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._handler.setFormatter(self._format)

    def addMessageInfo(self, msg):
        self._logger.info(msg)

    def addMessageError(self, msg):
        self._logger.error(msg)
