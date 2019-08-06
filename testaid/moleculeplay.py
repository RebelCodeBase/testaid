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
import json
import os
from pathlib import Path
import shutil


class MoleculePlay(object):
    '''Run ansible playbooks against molecule host using the ansible python api.

    Methods:
        get_project_dir()
            return the ansible project dir as pathlib.Path

        get_roles()
            return a list of roles by gathering the subdirs of the roles dir

        get_vars()
            return a dict of ansible vars including ansible_facts
            by running a playbook against a molecule host

        get_vars_from_files()
            return a dict of ansible variables fast without running a playbook

        create_playbook(gather_facts=True, gather_roles=True)
            create a playbook with ansible_facts and roles which won't run

        run_playbook(playbook)
            run a playbook against a molecule host
    '''
    def __init__(self):
        # Leverage the ansible python api
        # to run a playbook against a molecule host.
        #
        # see: ansible python api
        # https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html
        try:
            self.molecule_ephemeral_directory = \
                Path(os.environ['MOLECULE_EPHEMERAL_DIRECTORY'])
            self.molecule_scenario_directory = \
                Path(os.environ['MOLECULE_SCENARIO_DIRECTORY'])
        except KeyError:
            # return None if we can't access the molecule environment variables
            return None

        # create symlink in molecule ephemeral directory
        # to roles directory in project dir
        self._create_symlink_('roles')

        # use molecule managed inventory
        inventory_file = self.molecule_ephemeral_directory / \
                         'inventory/ansible_inventory.yml'

        # FIXME: add TESTAID_EXTRA_VARS_FILES
        # inject extra_vars into ansible play with high weight
        self._extra_vars = dict()

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

        # use inventory host
        host = next(iter(self._inventory.hosts))

        # create a Host object
        self._host = Host(name=host)

    def get_host(self):
        return self._host
    
    def get_project_dir(self):
        '''Return ansible project dir.'''

        # start the ansible scenario directory
        path = self.molecule_scenario_directory

        # go up until you find the roles dir
        while path != Path('/'):
            path = path.parent
            if path / 'roles' in [d for d in path.iterdir() if d.is_dir()]:
                return path

        # else return None
        return None

    def get_roles(self):
        roles_dir = self.get_project_dir() / 'roles'
        roles = [d.name for d in roles_dir.iterdir() if d.is_dir()]
        return roles

    def read_vars(self, playbook):
        '''Return ansible variables without running a playbook.'''
        play = self._get_play_(playbook)
        ansible_vars = self._variable_manager.get_vars(play=play,
                                                      host=self._host)
        return ansible_vars

    def run_playbook(self, playbook):
        '''Run an ansible playbook using the ansible python api.'''
        play = self._get_play_(playbook)
        tqm = None
        self.results_callback = ResultCallback()

        try:
            tqm = TaskQueueManager(inventory=self._inventory,
                                   variable_manager=self._variable_manager,
                                   loader=self._loader,
                                   passwords=dict(),
                                   stdout_callback=self.results_callback)
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        return self.results_callback.result_playbook_run

    def _create_symlink_(self, path):
        '''Create symlink from molecule ephemeral dir to project dir.'''
        target = self.molecule_ephemeral_directory / path
        source = self.get_project_dir() / path
        try:
            target.symlink_to(source)
        except FileExistsError:
            pass

    def _get_play_(self, playbook):
        return Play().load(playbook,
                           variable_manager=self._variable_manager,
                           loader=self._loader,
                           vars=self._extra_vars)


class ResultCallback(CallbackBase):
    def __init__(self):
        self.result_playbook_run = list()

    def v2_runner_on_ok(self, result, **kwargs):
        self._clean_results(result._result, result._task.action)
        self.result_playbook_run.append(result._result)

    def v2_runner_on_failed(self, result, *args, **kwargs):
        # TODO: raise exception
        print('\n+++++++++++++++++++++++++++++++++++++++'
              '+++++++++++++++++++++++++++++++++++++++++')
        print('[ResultCallback::v2_runner_on_failed] '
              'Playbook failed! Is your molecule host up?')
        print('The result of the playbook run:')
        print(json.dumps(result._result, indent=4))
        print('+++++++++++++++++++++++++++++++++++++++++'
              '+++++++++++++++++++++++++++++++++++++++\n')
