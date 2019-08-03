class TestPass(object):
    '''Expose the ansible passwordstore plugin as pytest fixture'''
    def __init__(self, moleculebook):
        self._moleculebook = moleculebook
        self._moleculebook.create(gather_facts=False,
                                  gather_roles=False,
                                  host='localhost')
        self._lookup = "{{ lookup('passwordstore', \'" + path + "\')}}"
        self._moleculebook.add_task_debug(lookup)

    def testpass(self, path):
        return self._moleculebook.run()
