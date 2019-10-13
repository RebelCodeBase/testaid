class AnsibleRunError(Exception):
    '''Exception raised by MoleculePlay signals failed ansible playbook run.'''

    def __init__(self, msg, error):
        Exception.__init__(self, msg + '\n' + error)


class MoleculeBookRunError(Exception):
    '''Exception raised by MoleculeBook signals failed ansible playbook run.'''

    def __init__(self, msg):
        Exception.__init__(self, msg)


class TemplatesResolveError(Exception):
    '''Exception raised by TestVars signals failed ansible playbook run.'''

    def __init__(self, msg):
        Exception.__init__(self, msg)
