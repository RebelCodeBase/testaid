import os
import pytest
from testaid.moleculebook import MoleculeBook
from testaid.moleculeplay import MoleculePlay
from testaid.testpass import TestPass
from testaid.testvars import TestVars


@pytest.fixture(scope='session')
def moleculeplay():
    return MoleculePlay()


@pytest.fixture(scope='session')
def moleculebook(moleculeplay):
    return MoleculeBook(moleculeplay)


@pytest.fixture(scope='session')
def testpass(moleculebook):
    return TestPass(moleculebook).testpass


@pytest.fixture(scope='session')
def testvars(request, moleculebook):
    '''Expose ansible variables of a molecule test scenario.'''
    # Remember: it's easier to ask for forgiveness than permission
    # https://docs.python.org/3/glossary.html#term-eafp

    # determine the cache key which will determine if
    # two scenarios use the same or different cache values
    try:
        # try to get a molecule scenario-related cache key
        cache_key = 'testvars/' + os.environ['MOLECULE_EPHEMERAL_DIRECTORY']
    except KeyError:
        # use a global cache key as fallback
        cache_key = 'testvars/global'

    try:
        # determine if cache support is enabled in molecule
        # i.e. if the option "p: cacheprovider" is present in molecule.yml:
        # molecule -> verifier -> options
        testvars = request.config.cache.get(cache_key, None)
    except AttributeError:
        testvars = None

    if testvars is None:
        testvars = TestVars(moleculebook).get_testvars()

        try:
            # try to cache the testvars
            request.config.cache.set(cache_key, testvars)
        except AttributeError:
            pass

    return testvars
