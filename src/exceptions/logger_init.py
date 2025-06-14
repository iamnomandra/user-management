import logging

def logger():
    '''Initialize Logger'''    
    filename = "/Logs/app.log"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename=filename)
    logger = logging.getLogger(__name__)
    return logger
