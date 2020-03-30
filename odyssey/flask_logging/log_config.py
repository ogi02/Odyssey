import logging
from logging.handlers import RotatingFileHandler

info_log = logging.getLogger('info_log')
info_log.setLevel(logging.INFO)
error_log = logging.getLogger('error_log')
error_log.setLevel(logging.ERROR)

info_handling = RotatingFileHandler('./info.log', maxBytes = 1000, backupCount = 1)
error_handling = RotatingFileHandler('./error.log', maxBytes = 1000, backupCount = 1)

formatting = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
info_handling.setFormatter(formatting)
error_handling.setFormatter(formatting)

info_log.addHandler(info_handling)
error_log.addHandler(error_handling)