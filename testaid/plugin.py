import os
from pathlib import Path
import pytest
from testaid.moleculebook import MoleculeBook
from testaid.moleculeplay import MoleculePlay
from testaid.testpass import TestPass
from testaid.testvars import TestVars


def pytest_addoption(parser):
    parser.addoption("--testvars-no-gather-facts",
                     action="store_false",
                     default=True,
                     help="do not gather ansible_facts")
    parser.addoption("--testvars-no-resolve-vars",
                     action="store_false",
                     default=True,
                     help="do not resolve jinja2 templates")
    parser.addoption("--testvars-no-gather-molecule",
                     action="store_false",
                     default=True,
                     help="do not resolve molecule vars")
    parser.addoption("--testvars-no-extra-vars",
                     action="store_false",
                     default=True,
                     help="do not include extra vars")


###########################################################
# fixtures: command line options
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


###########################################################
# fixtures: environment variables
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
def testaid_extra_vars():
    '''environment variable TESTAID_EXTRA_VARS'''
    try:
        extra_vars = Path(os.environ['TESTAID_EXTRA_VARS'])
    except KeyError:
        extra_vars = ''
    return extra_vars


###########################################################
# fixtures: ansible python api
###########################################################


@pytest.fixture(scope='session')
def moleculeplay(molecule_ephemeral_directory,
                 molecule_scenario_directory):
    '''Expose ansible python api to run playbooks against a molecule host.'''
    return MoleculePlay(molecule_ephemeral_directory,
                        molecule_scenario_directory)


@pytest.fixture(scope='session')
def moleculebook(molecule_scenario_directory,
                 testaid_extra_vars,
                 moleculeplay):
    '''Run an ansible playbook against a molecule host.'''
    return MoleculeBook(molecule_scenario_directory,
                        testaid_extra_vars,
                        moleculeplay)


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
             gather_facts,
             resolve_vars,
             gather_molecule,
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
                            resolve_vars,
                            gather_facts,
                            gather_molecule,
                            extra_vars).get_testvars()
        try:
            # cache testvars
            request.config.cache.set(cache_key, testvars)
        except AttributeError:
            pass

    return testvars
