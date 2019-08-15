import json


class AnsibleRunError(Exception):
    '''Exception raised by MoleculePlay signals failed ansible playbook run.'''

    def __init__(self, result, msg, debug=False):
        error = msg
        if debug:
            error += "\n\n"
            error += json.dumps(result, indent=4)
        Exception.__init__(self, error)


class MoleculeBookRunError(Exception):
    '''Exception raised by MoleculeBook signals failed ansible playbook run.'''

    def __init__(self, result, msg, debug=False):
        error = msg
        if debug:
            error += "\n\n"
            error += json.dumps(result, indent=4)
        Exception.__init__(self, error)


class TemplatesResolveError(Exception):
    '''Exception raised by TestVars signals failed ansible playbook run.'''

    def __init__(self, msg):
        Exception.__init__(self, msg)
