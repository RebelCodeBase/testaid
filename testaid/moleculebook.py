import json
import testaid


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
        task_debug = dict(action=dict(module='debug', args=dict(msg=msg)))
        self._playbook['tasks'].append(task_debug)

    def run(self):
        return self._moleculeplay.run_playbook(self._playbook)

    def get_vars(self):
        '''Return ansible facts and vars of a molecule host.'''
        vars = dict()

        # self.create sets gather_facts=True by default so the ansible facts
        # of the default molecule host will be in result[0]['ansible_facts']
        self.create()

        # the ansible variables will be in result[1]['msg']
        self.add_task_debug('{{ vars }}')

        result = self.run()

        # create vars with vars['ansible_facts']
        try:
            vars = result[1]['msg']
            vars['ansible_facts'] = result[0]['ansible_facts']
        except IndexError:
            print('\n+++++++++++++++++++++++++++++++++++++++'
                  '+++++++++++++++++++++++++++++++++++++++++')
            print('[MoleculeBook::get_vars] '
                  'The ansible playbook run returned an unexpected result:')
            print(json.dumps(result, indent=4))
            print('+++++++++++++++++++++++++++++++++++++++++'
                  '+++++++++++++++++++++++++++++++++++++++\n')
        return vars

    def read_vars(self):
        '''Return ansible variables without running a playbook.'''
        self.create(gather_facts=False, host='localhost')
        vars = self._moleculeplay.read_vars(self._playbook)
        return vars
