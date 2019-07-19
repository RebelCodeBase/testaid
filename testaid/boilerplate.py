import os
import testinfra.utils.ansible_runner


def hosts():

    # if pytest is invoked directly (e.g. to run pytest --cache-clear)
    # molecule is not available so testinfra_hosts should be empty
    if 'MOLECULE_INVENTORY_FILE' in os.environ:
        return testinfra.utils.ansible_runner.AnsibleRunner(
            os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')
    else:
        return []
