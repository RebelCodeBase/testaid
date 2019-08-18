from ansible import context
from ansible.module_utils.common.collections import ImmutableDict
from ansible.playbook.play import Play
from testaid.ansiblerun import AnsibleRun


class MoleculePlay(object):
    '''Run ansible playbooks against molecule host using the ansible python api.
    '''
    def __init__(self,
                 ansibleloader,
                 ansibleinventory,
                 ansiblevarsmanager,
                 ansiblehost,
                 moleculeenv):
        # Leverage the ansible python api
        # to run a playbook against a molecule host.
        #
        # see: ansible python api
        # https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html

        self._moleculeenv = moleculeenv

        context.CLIARGS = ImmutableDict(connection='local',
                                        module_path=[''],
                                        forks=10,
                                        become=None,
                                        become_method=None,
                                        become_user=None,
                                        check=False,
                                        diff=False)
        self._loader = ansibleloader
        self._inventory = ansibleinventory
        self._variable_manager = ansiblevarsmanager
        self._host = ansiblehost

    def get_host(self):
        return self._host

    def get_molecule_scenario_directory(self):
        return self._moleculeenv.get_molecule_scenario_directory()

    def get_roles(self):
        return self._moleculeenv.get_roles()

    def read_vars(self, playbook):
        '''Return ansible variables without running a playbook.'''
        play = self._get_play_(playbook)
        ansible_vars = self._variable_manager.get_vars(play=play,
                                                       host=self._host)
        return ansible_vars

    def run_playbook(self, playbook):
        '''Run an ansible playbook using the ansible python api.'''
        play = self._get_play_(playbook)
        ansiblerun = AnsibleRun(self._inventory,
                                self._variable_manager,
                                self._loader)
        result = ansiblerun.run(play)
        return result

    def _get_play_(self, playbook):
        return Play().load(playbook,
                           variable_manager=self._variable_manager,
                           loader=self._loader)
