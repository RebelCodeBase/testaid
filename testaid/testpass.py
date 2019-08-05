class TestPass(object):
    '''Expose the ansible passwordstore plugin as pytest fixture'''
    def __init__(self, moleculebook):
        self._moleculebook = moleculebook
        self._moleculebook.create(gather_facts=False,
                                  gather_roles=False,
                                  host='localhost')

    def testpass(self, path):
        lookup = "{{ lookup('passwordstore', \'" + path + "\')}}"
        self._moleculebook.add_task_debug(lookup)
        return self._moleculebook.run()[0]['msg']
