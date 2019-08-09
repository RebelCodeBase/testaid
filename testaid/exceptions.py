import json


class MoleculeBookRunFailed(Exception):
    '''Exception raised by MoleculeBook signals failed ansible playbook run.'''

    def __init__(self, result, msg, debug=False):
        self._result = result
        self._msg = msg
        self._debug = debug

    def __str__(self):
        error = self._msg
        if self._debug:
            error += "\n\n"
            error += json.dumps(self._result, indent=4)
        return error
