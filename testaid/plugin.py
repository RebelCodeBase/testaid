import os
import pytest
from testaid.testpass import Testpass
from testaid.testvars import Testvars


@pytest.fixture()
def testpass(host):
    return Testpass(host).testpass


@pytest.fixture()
def testvars(request, host, tmp_path):
    # Remember: it's easier to ask for forgiveness than permission
    # https://docs.python.org/3/glossary.html#term-eafp

    # determine the cache key which will determine if
    # two scenarios use the same or different cache values
    try:
        # try to get a molecule scenario-related cache key
        cache_key = 'testvars/' + os.environ['MOLECULE_EPHEMERAL_DIRECTORY']
    except:
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
        testvars = Testvars(host, tmp_path).testvars

        try:
            # try to cache the testvars
            request.config.cache.set(cache_key, testvars)
        except AttributeError:
            pass

    return testvars
