import ansible.constants as C
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import shutil
from testaid.exceptions import AnsibleRunError


class AnsibleRun(object):

    def __init__(self,
                 inventory,
                 variable_manager,
                 loader):
        self._inventory = inventory
        self._variable_manager = variable_manager
        self._loader = loader

    def run(self, play):
        tqm = None
        rc = ResultCallback()
        try:
            tqm = TaskQueueManager(inventory=self._inventory,
                                   variable_manager=self._variable_manager,
                                   loader=self._loader,
                                   passwords=dict(),
                                   stdout_callback=rc)
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        if rc.failed_playbook_run:
            raise AnsibleRunError(
                rc.result_playbook_run,
                'Unable to run playbook. Is your host up?')
        return rc.result_playbook_run


class ResultCallback(CallbackBase):

    def __init__(self):
        super(ResultCallback, self).__init__()
        self.result_playbook_run = list()
        self.failed_playbook_run = False

    def v2_runner_on_ok(self, result, **kwargs):
        self._clean_results(result._result, result._task.action)
        self.result_playbook_run.append(result._result)

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self._clean_results(result._result, result._task.action)
        self.result_playbook_run.append(result._result)
        self.failed_playbook_run = True
