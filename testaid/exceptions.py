import json


class MoleculePlayRunFailed(Exception):
    '''Exception raised by MoleculePlay signals failed ansible playbook run.'''

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


class TemplatesResolveFailed(Exception):
    '''Exception raised by TestVars signals failed ansible playbook run.'''

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg
