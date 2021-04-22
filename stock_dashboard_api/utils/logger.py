import logging
import os
from logging.config import fileConfig

LOGGING_CONF = os.getenv('LOGGING_CONF')
fileConfig(LOGGING_CONF, disable_existing_loggers=True)
views_logger = logging.getLogger('views')
