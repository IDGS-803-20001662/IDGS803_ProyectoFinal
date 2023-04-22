import logging

class Logger:
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        self.file_handler = logging.FileHandler('{}.log'.format(self.name))
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        
    def debug(self, message):
        self.logger.debug(message) # Acción normal del sistema
        
    def info(self, message):
        self.logger.info(message) # Información del sistema
        
    def warning(self, message):
        self.logger.warning(message) # Advertencia de una acción normal del sistema
        
    def error(self, message):
        self.logger.error(message) # Error de una acción normal del sistema
        
    def critical(self, message):
        self.logger.critical(message) # Error en la aplicación
        
    def exception(self, message):
        self.logger.exception(message) # Excepción en la aplicación
        
    def log(self, message):
        self.logger.info(message) # Otro tipo de logs