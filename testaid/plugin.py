import os
import pytest
from testaid.testpass import Testpass
from testaid.testvars import Testvars


@pytest.fixture(scope='module')
def testpass(host):
    return Testpass(host).testpass


@pytest.fixture(scope='module')
def testvars(request, host):
    try:
        cache_id = 'testvars' + os.environ['MOLECULE_EPHEMERAL_DIRECTORY']
    except:
        cache_id = 'testvars/global'
    testvars = request.config.cache.get(cache_id, None)
    if testvars is None:
        testvars = Testvars(host).testvars
        request.config.cache.set(cache_id, testvars)
    return testvars
