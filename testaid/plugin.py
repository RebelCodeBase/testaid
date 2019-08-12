import os
from pathlib import Path
import pytest
from testaid.moleculeenv import MoleculeEnv
from testaid.moleculeplay import MoleculePlay
from testaid.moleculebook import MoleculeBook
from testaid.templates import Templates
from testaid.jsonvars import JsonVars
from testaid.jsonvarsdebug import JsonVarsDebug
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
                     "--testvars-no-gather-molecule",
                     action="store_false",
                     default=True,
                     help="do not resolve molecule vars")
    testvars_optiongroup.addoption(
                     "--testvars-no-extra-vars",
                     action="store_false",
                     default=True,
                     help="do not include extra vars")


###########################################################
# fixtures: testvars options
###########################################################


@pytest.fixture(scope='session')
def resolve_vars(request):
    '''testvars option --testvars-no-resolve-vars'''
    return request.config.getoption("--testvars-no-resolve-vars")


@pytest.fixture(scope='session')
def gather_facts(request):
    '''testvars option --testvars-no-gather-facts'''
    return request.config.getoption("--testvars-no-gather-facts")


@pytest.fixture(scope='session')
def gather_molecule(request):
    '''testvars option --testvars-no-gather-molecule'''
    return request.config.getoption("--testvars-no-gather-molecule")


@pytest.fixture(scope='session')
def extra_vars(request):
    '''testvars option --testvars-no-extra-vars'''
    return request.config.getoption("--testvars-no-extra-vars")


@pytest.fixture(scope='session')
def testvars_extra_vars():
    '''environment variable TESTVARS_EXTRA_VARS'''
    try:
        extra_vars = Path(os.environ['TESTVARS_EXTRA_VARS'])
    except KeyError:
        extra_vars = ''
    return extra_vars


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
                molecule_scenario_directory):
    return MoleculeEnv(molecule_ephemeral_directory,
                       molecule_scenario_directory)


###########################################################
# fixtures: ansible python api
###########################################################


@pytest.fixture(scope='session')
def moleculeplay(moleculeenv, inventory_file):
    '''Expose ansible python api to run playbooks against a molecule host.'''
    return MoleculePlay(moleculeenv,
                        inventory_file)


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
def templates(moleculebook):
    return Templates(moleculebook)


@pytest.fixture(scope='session')
def jsonvarsdebug():
    return JsonVarsDebug()


@pytest.fixture(scope='session')
def jsonvars(jsonvarsdebug, templates, gather_molecule):
    return JsonVars(jsonvarsdebug, templates, gather_molecule)


###########################################################
# fixtures: molecule/testinfra/ansible helpers
###########################################################


@pytest.fixture(scope='session')
def testpass(moleculebook):
    '''Provide access to the ansible passwordstore lookup plugin.'''
    return TestPass(moleculebook).testpass


@pytest.fixture(scope='session')
def testvars(request,
             molecule_ephemeral_directory,
             moleculebook,
             jsonvars,
             resolve_vars,
             gather_facts,
             extra_vars):
    '''Expose ansible variables and facts of a molecule test scenario.'''
    # molecule_ephemeral_directory should be unique for each scenario
    cache_key = str('testvars' / molecule_ephemeral_directory)

    try:
        # read testvars from cache
        # you can enable cache support in molecule.yml:
        # molecule -> verifier -> options
        # option "p: cacheprovider"
        testvars = request.config.cache.get(cache_key, None)
    except AttributeError:
        testvars = None

    if testvars is None:
        testvars = TestVars(moleculebook,
                            jsonvars,
                            resolve_vars,
                            gather_facts,
                            extra_vars).get_testvars()
        try:
            # cache testvars
            request.config.cache.set(cache_key, testvars)
        except AttributeError:
            pass

    return testvars
