import os
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
def moleculeplay():
    '''Expose ansible python api to run playbooks against a molecule host.'''
    return MoleculePlay()


@pytest.fixture(scope='session')
def moleculebook(moleculeplay):
    '''Run an ansible playbook against a molecule host.'''
    return MoleculeBook(moleculeplay)


@pytest.fixture(scope='session')
def testpass(moleculebook):
    '''Provide access to the ansible passwordstore lookup plugin.'''
    return TestPass(moleculebook).testpass


@pytest.fixture(scope='session')
def testvars(request,
             moleculebook,
             gather_facts,
             resolve_vars,
             gather_molecule,
             extra_vars):
    '''Expose ansible variables and facts of a molecule test scenario.'''
    # remember: it's easier to ask for forgiveness than permission
    # https://docs.python.org/3/glossary.html#term-eafp

    # set the scope of the cache key
    # MOLECULE_EPHEMERAL_DIRECTORY should be unique for each molecule scenario
    try:
        # try to get a molecule scenario-scoped cache key
        cache_key = 'testvars/' + os.environ['MOLECULE_EPHEMERAL_DIRECTORY']
    except KeyError:
        # use a global cache key as fallback
        cache_key = 'testvars/global'

    try:
        # check if cache support is enabled in molecule
        # i.e. if the option "p: cacheprovider" is present in molecule.yml:
        # molecule -> verifier -> options
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
            # try to cache the testvars
            request.config.cache.set(cache_key, testvars)
        except AttributeError:
            pass

    return testvars
