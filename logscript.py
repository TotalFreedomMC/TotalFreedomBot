import logging

logging.basicConfig(level=logging.CRITICAL, format='%(message)s',handlers=[logging.FileHandler('log.log', 'a')])
