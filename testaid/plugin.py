import os
import pytest
from testaid.testpass import Testpass
from testaid.testvars import Testvars


@pytest.fixture()
def testpass(host):
    return Testpass(host).testpass


@pytest.fixture()
def testvars(request, host, tmp_path):
    try:
        cache_key = 'testvars/' + os.environ['MOLECULE_EPHEMERAL_DIRECTORY']
    except:
        cache_key = 'testvars/global'
    testvars = request.config.cache.get(cache_key, None)
    if testvars is None:
        testvars = Testvars(host, tmp_path).testvars
        request.config.cache.set(cache_key, testvars)
    return testvars
