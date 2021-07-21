import traceback
import logging

try:
    doSomething()
except Exception as e:
    logging.error(traceback.format_exc())