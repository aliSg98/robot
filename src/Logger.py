import logging

class Logger:
    def __init__(self,level=logging.INFO):
        self._logger = logging.getLogger('log')
        self._logger.setLevel(level)
        self._handler = logging.FileHandler(r"C:\Users\nasudre\Desktop\Robot\LOG\log.txt")
        self._handler.setLevel(level)
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._handler.setFormatter(format)
        self._logger.addHandler(self._handler)

    def setMessage(self, msg, level): 
        if level.lower() == 'info':
            self._logger.info(msg)
        elif level.lower() == 'debug':
            self._logger.debug(msg)
        elif level.lower() == 'error':
            self._logger.error(msg)
        elif level.lower() == 'critical':
            self._logger.error(msg)
        elif level.lower() == 'warning':
            self._logger.error(msg)
        else:
            raise ValueError("Level de logging no soportado")
