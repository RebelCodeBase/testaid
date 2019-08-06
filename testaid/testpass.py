class TestPass(object):
    '''Expose the ansible passwordstore plugin as pytest fixture'''
    def __init__(self, moleculebook):
        self._moleculebook = moleculebook

    def testpass(self, path):

        # reset playbook
        self._moleculebook.create(gather_facts=False,
                                  gather_roles=False,
                                  host='localhost')
        lookup = "{{ lookup('passwordstore', \'" + path + "\')}}"
        self._moleculebook.add_task_debug(lookup)
        result = self._moleculebook.run()[0]['msg']
        return result
