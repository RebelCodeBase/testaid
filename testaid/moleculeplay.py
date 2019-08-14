from ansible import context
from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.vars.manager import VariableManager
from testaid.ansiblerun import AnsibleRun


class MoleculePlay(object):
    '''Run ansible playbooks against molecule host using the ansible python api.
    '''
    def __init__(self,
                 moleculeenv,
                 inventory_file):
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
        self._loader = DataLoader()
        self._inventory = InventoryManager(loader=self._loader,
                                           sources=str(inventory_file))
        self._variable_manager = VariableManager(loader=self._loader,
                                                 inventory=self._inventory)
        try:
            # use inventory host
            host = next(iter(self._inventory.hosts))
        except StopIteration:
            host = 'localhost'

        # create a Host object
        self._host = Host(name=host)

    def get_host(self):
        return self._host

    def get_molecule_scenario_directory(self):
        return self._moleculeenv.get_molecule_scenario_directory()

    def get_roles(self):
        return self._moleculeenv.get_roles()

    def read_vars(self, playbook):
        '''Return ansible variables without running a playbook.'''
        play = self._get_play_(playbook)
        host = self.get_host()
        variable_manager = self._get_variable_manager_()
        ansible_vars = variable_manager.get_vars(play=play,
                                                 host=host)
        return ansible_vars

    def run_playbook(self, playbook):
        '''Run an ansible playbook using the ansible python api.'''
        play = self._get_play_(playbook)
        self._ansiblerun = AnsibleRun(self._inventory,
                                      self._variable_manager,
                                      self._loader)
        result = self._ansiblerun.run(play)
        return result

    def _get_inventory_(self):
        return self._inventory

    def _get_loader_(self):
        return self._loader

    def _get_play_(self, playbook):
        variable_manager = self._get_variable_manager_()
        loader = self._get_loader_()
        play = Play().load(playbook,
                           variable_manager=variable_manager,
                           loader=loader)
        return play

    def _get_variable_manager_(self):
        return self._variable_manager


