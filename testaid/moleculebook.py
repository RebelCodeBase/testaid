import json


class MoleculeBook(object):
    '''Run an ansible playbook against a molecule host'''

    def __init__(self, moleculeplay):
        self._moleculeplay = moleculeplay
        if self._moleculeplay is None:
            return None
        self._playbook = self.create()

    def get(self):
        return self._playbook

    def set(self, playbook):
        self._playbook = playbook

    def create(self,
               gather_facts=True,
               gather_roles=True,
               host=None):
        '''Create an ansible playbook using the ansible python api.'''
        if host is None:
            host = self._moleculeplay.get_host()

        playbook = dict(
            name="ansible playbook",
            hosts=str(host),
            gather_facts=str(gather_facts),
            tasks=list(),
            roles=list(),
        )

        if gather_roles:
            for role in self._moleculeplay.get_roles():
                playbook['roles'].append(dict(name=role, when='False'))

        self._playbook = playbook

    def add_task_debug(self, msg):
        task = dict(action=dict(module='debug', args=dict(msg=msg)))
        self._playbook['tasks'].append(task)

    def add_task_set_fact(self, key, value):
        args = {key: value}
        task = dict(action=dict(module='set_fact', args=args))
        self._playbook['tasks'].append(task)

    def run(self):
        return self._moleculeplay.run_playbook(self._playbook)

    def get_vars(self, run_playbook=True, gather_facts=True):
        '''Return ansible facts and vars of a molecule host.

        Args:
            run_playbook (bool): run playbooks to gather and resolve vars?
                Defaults to True.
                A playbook will be run
                - with ``gather_facts:true`` if gather_facts arg is True
                - to invoke the ansible debug module to resolve "{{ vars }}"
                - to invoke different playbook to resolve the vars
                If False the ansible variables will be gathered
                by the ansible VariableManager offline.
                If False it conflicts with gather_facts=True
                If False no templates will be resolved
            gather_facts (bool): gather ansible_facts from a molecule host?
                Defaults to True.
                A playbook will be run with ``gather_facts:true``.

        Returns:
            vars (dict): resolved ansible variables and facts
        '''
        vars = dict()

        if not run_playbook:
            return self._read_vars()

        # self.create sets gather_facts=True by default so the ansible facts
        # of the default molecule host will be in result[0]['ansible_facts']
        self.create(gather_facts=gather_facts)

        # the ansible variables will be in result[1]['msg']
        self.add_task_debug('{{ vars }}')

        result = self.run()

        # create vars with vars['ansible_facts']
        try:
            if gather_facts:
                vars = result[1]['msg']
                vars['ansible_facts'] = result[0]['ansible_facts']
            else:
                vars = result[0]['msg']
        except IndexError:
            # TODO: raise exception
            print('\n+++++++++++++++++++++++++++++++++++++++'
                  '+++++++++++++++++++++++++++++++++++++++++')
            print('[MoleculeBook::get_vars] '
                  'The ansible playbook run returned an unexpected result:')
            print(json.dumps(result, indent=4))
            print('+++++++++++++++++++++++++++++++++++++++++'
                  '+++++++++++++++++++++++++++++++++++++++\n')
        return vars

    def _read_vars(self):
        '''Return ansible variables without running a playbook.'''
        self.create(gather_facts=False, host='localhost')
        vars = self._moleculeplay.read_vars(self._playbook)
        return vars
