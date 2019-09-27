from testaid.exceptions import MoleculeBookRunError


class MoleculeBook(object):
    '''Run an ansible playbook against a molecule host'''

    def __init__(self,
                 testvars_extra_vars,
                 moleculeplay):
        self._moleculeplay = moleculeplay
        self._testvars_extra_vars = testvars_extra_vars
        self._playbook = dict()
        self.create()

    def get(self):
        '''Get the ansible playbook'''
        return self._playbook

    def set(self, playbook):
        '''Set an ansible playbook'''
        self._playbook = playbook

    def create(self,
               gather_facts=True,
               gather_roles=True,
               extra_vars=True,
               host=None):
        '''Create an ansible playbook using the ansible python api.'''
        if host is None:
            host = self._moleculeplay.get_host()

        playbook = dict(
            name="ansible playbook",
            hosts=str(host),
            gather_facts=str(gather_facts),
            vars_files=list(),
            roles=list(),
            tasks=list(),
        )

        # include extra vars files
        if extra_vars:
            for path in self._get_extra_vars_():
                playbook['vars_files'].append(str(path))

        # include roles
        if gather_roles:
            for role in self._moleculeplay.get_roles():
                playbook['roles'].append(dict(name=role, when='False'))

        self._playbook = playbook

    def add_task_debug(self, msg):
        '''Add a task using the ansible debug module'''
        task = dict(action=dict(module='debug', args=dict(msg=msg)))
        self._playbook['tasks'].append(task)

    def add_task_include_vars_dir(self, vars_dir):
        '''Add a task using the ansible include_vars module'''
        args = dict(dir=str(vars_dir))
        task = dict(action=dict(module='include_vars', args=args))
        self._playbook['tasks'].append(task)

    def get_vars(self, run_playbook=True, gather_facts=True, extra_vars=True):
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
            extra_vars (bool): include extra vars from vars files?
                Defaults to True.
                An include_vars task will be added to include extra vars files
                specified in the environment variable TESTVARS_EXTRA_VARS

        Returns:
            vars (dict): resolved ansible variables and facts
        '''
        vars = dict()

        if not run_playbook:
            return self._read_vars_()

        # self.create sets gather_facts=True by default so the ansible facts
        # of the default molecule host will be in result[0]['ansible_facts']
        self.create(gather_facts=gather_facts, extra_vars=extra_vars)

        # the ansible variables will be in result[1]['msg']
        self.add_task_debug('{{ vars }}')

        result = self.run()

        # create vars with vars['ansible_facts']
        if gather_facts:
            try:
                vars = result[1]['msg']
                vars['ansible_facts'] = result[0]['ansible_facts']
            except (IndexError, KeyError):
                raise MoleculeBookRunError(
                    result,
                    'Unable to gather ansible vars and facts.')
        else:
            try:
                vars = result[0]['msg']
            except (IndexError, KeyError):
                raise MoleculeBookRunError(
                    result,
                    'Unable to gather ansible vars.')
        return vars

    def run(self):
        '''Run the ansible playbook'''
        return self._moleculeplay.run_playbook(self._playbook)

    def _get_extra_vars_(self):
        return self._testvars_extra_vars

    def _get_molecule_scenario_directory_(self):
        return self._moleculeplay.get_molecule_scenario_directory()

    def _read_vars_(self):
        '''Return ansible variables without running a playbook.'''
        self.create(gather_facts=False, host='localhost')
        vars = self._moleculeplay.read_vars(self._playbook)
        return vars
