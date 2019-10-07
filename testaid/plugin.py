import os
from pathlib import Path
import pytest
from testaid.ansibleres import AnsibleLoader
from testaid.ansibleres import AnsibleInventory
from testaid.ansibleres import AnsibleVarsManager
from testaid.ansibleres import AnsibleLocalHost
from testaid.ansibleres import AnsibleHost
from testaid.moleculeenv import MoleculeEnv
from testaid.moleculeplay import MoleculePlay
from testaid.moleculebook import MoleculeBook
from testaid.templates import Templates
from testaid.jsonvars import JsonVars
from testaid.jsonvarsdebug import JsonVarsDebug
from testaid.pathlist import PathList
from testaid.testpass import TestPass
from testaid.testvars import TestVars


###########################################################
# command line options: testvars group
###########################################################


def pytest_addoption(parser):
    testvars_optiongroup = parser.getgroup("testvars")
    testvars_optiongroup.addoption(
                     "--testvars-no-gather-facts",
                     action="store_false",
                     default=True,
                     help="do not gather ansible_facts")
    testvars_optiongroup.addoption(
                     "--testvars-no-resolve-vars",
                     action="store_false",
                     default=True,
                     help="do not resolve jinja2 templates")
    testvars_optiongroup.addoption(
                     "--testvars-no-gatherfrom-moleculehost",
                     action="store_false",
                     default=True,
                     help="do not gather vars from molecule host")
    testvars_optiongroup.addoption(
                     "--testvars-no-gather-molecule",
                     action="store_false",
                     default=True,
                     help="do not resolve molecule vars")
    testvars_optiongroup.addoption(
                     "--testvars-no-gather-roles",
                     action="store_false",
                     default=True,
                     help="do not gather vars from roles")
    testvars_optiongroup.addoption(
                     "--testvars-no-extra-vars",
                     action="store_false",
                     default=True,
                     help="do not include extra vars")
    testvars_optiongroup.addoption(
                     "--testvars-no-resolvevia-localhost",
                     action="store_false",
                     default=True,
                     help="do not resolve vars by using localhost")


###########################################################
# fixtures: testvars option booleans
###########################################################


@pytest.fixture(scope='session')
def resolve_vars(request):
    '''testvars option --testvars-no-resolve-vars'''
    return request.config.getoption("--testvars-no-resolve-vars")


@pytest.fixture(scope='session')
def gatherfrom_moleculehost(request):
    '''testvars option --testvars-no-gatherfrom-moleculehost'''
    return request.config.getoption("--testvars-no-gatherfrom-moleculehost")


@pytest.fixture(scope='session')
def gather_facts(request):
    '''testvars option --testvars-no-gather-facts'''
    return request.config.getoption("--testvars-no-gather-facts")


@pytest.fixture(scope='session')
def gather_molecule(request):
    '''testvars option --testvars-no-gather-molecule'''
    return request.config.getoption("--testvars-no-gather-molecule")


@pytest.fixture(scope='session')
def gather_roles(request):
    '''testvars option --testvars-no-gather-roles'''
    return request.config.getoption("--testvars-no-gather-roles")


@pytest.fixture(scope='session')
def extra_vars(request):
    '''testvars option --testvars-no-extra-vars'''
    return request.config.getoption("--testvars-no-extra-vars")


@pytest.fixture(scope='session')
def resolvevia_localhost(request):
    '''testvars option --testvars-no-resolvevia-localhost'''
    return request.config.getoption("--testvars-no-resolvevia-localhost")


###########################################################
# fixtures: testvars option lists
###########################################################


@pytest.fixture(scope='session')
def testvars_roles_blacklist(molecule_scenario_directory):
    '''environment variable TESTVARS_ROLES_BLACKLIST'''
    try:
        blacklist = os.environ['TESTVARS_ROLES_BLACKLIST']
    except KeyError:
        return list()
    return blacklist.split(':')


@pytest.fixture(scope='session')
def testvars_roles_whitelist(molecule_scenario_directory):
    '''environment variable TESTVARS_ROLES_WHITELIST'''
    try:
        whitelist = os.environ['TESTVARS_ROLES_WHITELIST']
    except KeyError:
        return list()
    return whitelist.split(':')


@pytest.fixture(scope='session')
def testvars_extra_vars(molecule_scenario_directory):
    '''environment variable TESTVARS_EXTRA_VARS'''
    try:
        extra_vars = Path(os.environ['TESTVARS_EXTRA_VARS'])
    except KeyError:
        return list()
    return PathList(extra_vars,
                    molecule_scenario_directory).get()


###########################################################
# fixtures: ansible resources
###########################################################


@pytest.fixture(scope='session')
def ansibleloader():
    return AnsibleLoader().get()


@pytest.fixture(scope='session')
def ansibleinventory(ansibleloader,
                     inventory_file):
    return AnsibleInventory(ansibleloader,
                            inventory_file).get()


@pytest.fixture(scope='session')
def ansiblevarsmanager(ansibleloader,
                       ansibleinventory):
    return AnsibleVarsManager(ansibleloader,
                              ansibleinventory).get()


@pytest.fixture(scope='session')
def ansiblelocalhost():
    return AnsibleLocalHost().get()


@pytest.fixture(scope='session')
def ansiblehost(ansibleinventory):
    return AnsibleHost(ansibleinventory).get()


###########################################################
# fixtures: molecule resources
###########################################################


@pytest.fixture(scope='session')
def molecule_ephemeral_directory(tmp_path_factory):
    '''environment variable MOLECULE_EPHEMERAL_DIRECTORY'''
    try:
        dir = Path(os.environ['MOLECULE_EPHEMERAL_DIRECTORY'])
    except KeyError:
        dir = tmp_path_factory.mktemp('molecule_ephemeral_directory')
    return dir


@pytest.fixture(scope='session')
def molecule_scenario_directory(tmp_path_factory):
    '''environment variable MOLECULE_SCENARIO_DIRECTORY'''
    try:
        dir = Path(os.environ['MOLECULE_SCENARIO_DIRECTORY'])
    except KeyError:
        dir = tmp_path_factory.mktemp('molecule_scenario_directory')
    return dir


@pytest.fixture(scope='session')
def inventory_file(molecule_ephemeral_directory):
    '''Molecule managed ansible inventory file.'''
    inventory_file = molecule_ephemeral_directory / \
        'inventory/ansible_inventory.yml'
    inventory_dir = molecule_ephemeral_directory / 'inventory'
    inventory_dir.mkdir(exist_ok=True)
    if not inventory_file.is_file():
        inventory = "localhost"
        inventory_file.write_text(inventory)
    return inventory_file


@pytest.fixture(scope='session')
def moleculeenv(molecule_ephemeral_directory,
                molecule_scenario_directory,
                gather_roles,
                testvars_roles_blacklist,
                testvars_roles_whitelist):
    return MoleculeEnv(molecule_ephemeral_directory,
                       molecule_scenario_directory,
                       gather_roles,
                       testvars_roles_blacklist,
                       testvars_roles_whitelist)


###########################################################
# fixtures: ansible python api
###########################################################


@pytest.fixture(scope='session')
def moleculelocalplay(ansibleloader,
                      ansibleinventory,
                      ansiblevarsmanager,
                      ansiblelocalhost,
                      moleculeenv):
    '''Expose ansible python api to run playbooks against a molecule host.'''
    return MoleculePlay(ansibleloader,
                        ansibleinventory,
                        ansiblevarsmanager,
                        ansiblelocalhost,
                        moleculeenv)


@pytest.fixture(scope='session')
def moleculelocalbook(testvars_extra_vars,
                      moleculelocalplay):
    '''Run an ansible playbook against a molecule host.'''
    return MoleculeBook(testvars_extra_vars,
                        moleculelocalplay)


@pytest.fixture(scope='session')
def moleculeplay(ansibleloader,
                 ansibleinventory,
                 ansiblevarsmanager,
                 ansiblehost,
                 moleculeenv):
    '''Expose ansible python api to run playbooks against a molecule host.'''
    return MoleculePlay(ansibleloader,
                        ansibleinventory,
                        ansiblevarsmanager,
                        ansiblehost,
                        moleculeenv)


@pytest.fixture(scope='session')
def moleculebook(testvars_extra_vars,
                 moleculeplay):
    '''Run an ansible playbook against a molecule host.'''
    return MoleculeBook(testvars_extra_vars,
                        moleculeplay)


###########################################################
# fixtures: testvars helpers
###########################################################


@pytest.fixture(scope='session')
def localtemplates(moleculelocalbook):
    return Templates(moleculelocalbook)


@pytest.fixture(scope='session')
def templates(moleculebook):
    return Templates(moleculebook)


@pytest.fixture(scope='session')
def jsonvarsdebug():
    return JsonVarsDebug()


@pytest.fixture(scope='session')
def jsonvars(jsonvarsdebug,
             localtemplates,
             templates,
             resolvevia_localhost,
             gather_molecule):
    return JsonVars(jsonvarsdebug,
                    localtemplates,
                    templates,
                    resolvevia_localhost,
                    gather_molecule)


@pytest.fixture(scope='session')
def cache_key(molecule_ephemeral_directory):
    # molecule_ephemeral_directory should be unique for each scenario
    return 'testvars' + str(molecule_ephemeral_directory)


###########################################################
# fixtures: molecule/testinfra/ansible helpers
###########################################################


@pytest.fixture(scope='session')
def testpass(moleculebook):
    '''Provide access to the ansible passwordstore lookup plugin.'''
    return TestPass(moleculebook).testpass


@pytest.fixture(scope='session')
def testvars(request,
             moleculebook,
             jsonvars,
             resolve_vars,
             gatherfrom_moleculehost,
             gather_facts,
             extra_vars,
             cache_key):
    '''Expose ansible variables and facts of a molecule test scenario.'''
    testvars = TestVars.get_cache(request, cache_key)
    if testvars is None:
        testvars_object = TestVars(
                 moleculebook,
                 jsonvars,
                 resolve_vars,
                 gatherfrom_moleculehost,
                 gather_facts,
                 extra_vars)
        testvars = testvars_object.get_testvars()
        testvars_object.set_cache(request, cache_key)
    return testvars
