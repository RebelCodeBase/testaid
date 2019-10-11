from io import StringIO
import logging
from molecule import util
import os


class MoleculeLog(object):

    def __init__(self):
        self._log_stream = StringIO()
        handler = logging.StreamHandler(self._log_stream)
        self._logger = logging.getLogger('testaid')
        self._logger.handlers = []
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)

    def debug(self, msg):
        self._logger.debug(msg)

    def get_log(self):
        return self._log_stream.getvalue()

    def print_debug(self):
        testaid_env = \
            {k: v for (k, v) in os.environ.items() if 'TESTVARS_' in k}
        if testaid_env:
            print('\n')
            util.print_debug('TESTVARS ENVIRONMENT',
                             util.safe_dump(testaid_env))
        log = self.get_log()
        if log:
            if not testaid_env:
                print('\n')
            util.print_debug('TESTVARS LOG', log)
