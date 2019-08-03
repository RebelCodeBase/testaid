import pytest
from ruamel.yaml import YAML
import sys
import testaid

testinfra_hosts = testaid.hosts()
yaml = YAML()

# print testvars as yaml
# @pytest.mark.debug
@pytest.mark.skip
def test_testaid_debug(host, testvars, testpass):
    print('\n*******************')
    yaml.dump(testvars, sys.stdout)
    print('*******************\n')
    assert False
