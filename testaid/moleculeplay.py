import ansible.constants as C
from ansible import context
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
import shutil
from testaid.exceptions import MoleculePlayRunFailed


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
        tqm = None
        inventory = self._get_inventory_()
        variable_manager = self._get_variable_manager_()
        loader = self._get_loader_()
        results_callback = ResultCallback()
        play = self._get_play_(playbook)
        try:
            tqm = TaskQueueManager(inventory=inventory,
                                   variable_manager=variable_manager,
                                   loader=loader,
                                   passwords=dict(),
                                   stdout_callback=results_callback)
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        return results_callback.result_playbook_run

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


class ResultCallback(CallbackBase):

    def __init__(self):
        super(ResultCallback, self).__init__()
        self.result_playbook_run = list()

    def v2_runner_on_ok(self, result, **kwargs):
        self._clean_results(result._result, result._task.action)
        self.result_playbook_run.append(result._result)

    def v2_runner_on_failed(self, result, *args, **kwargs):
        raise MoleculePlayRunFailed(
            result._result,
            'Unable to run playbook. Is your host up?')
