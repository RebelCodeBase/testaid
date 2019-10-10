from io import StringIO
import logging


class MoleculeLog(object):

    def __init__(self):
        self._log_stream = StringIO()
        handler = logging.StreamHandler(self._log_stream)
        self._logger = logging.getLogger('testaid')
        self._logger.handlers = []
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)

    def get_log(self):
        return self._log_stream.getvalue()

    def debug(self, msg):
        self._logger.debug(msg)
