from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager


class AnsibleLoader(object):

    def __init__(self):
        pass

    def get(self):
        return DataLoader()


class AnsibleInventory(object):

    def __init__(self,
                 loader,
                 inventoryfile):
        self._inventory = InventoryManager(loader=loader,
                                           sources=str(inventoryfile))

    def get(self):
        return self._inventory


class AnsibleVarsManager(object):

    def __init__(self,
                 loader,
                 inventory):
        self._variable_manager = VariableManager(loader=loader,
                                                 inventory=inventory)

    def get(self):
        return self._variable_manager


class AnsibleLocalHost(object):

    def __init__(self):
        host = 'localhost'
        self._host = Host(name=host)

    def get(self):
        return self._host


class AnsibleHost(object):

    def __init__(self, inventory):
        host = next(iter(inventory.hosts))
        self._host = Host(name=host)

    def get(self):
        return self._host
