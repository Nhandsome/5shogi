from utils.setup_logger import setup_logger

LOGGER_DISABLED = {
'main':False
, 'memory':False
, 'model': False}



logger_main = setup_logger('logger_main', 'logs/logger_main.log')
logger_main.disabled = LOGGER_DISABLED['main']

logger_memory = setup_logger('logger_memory', 'logs/logger_memory.log')
logger_memory.disabled = LOGGER_DISABLED['memory']

logger_model = setup_logger('logger_model', 'logs/logger_model.log')
logger_model.disabled = LOGGER_DISABLED['model']