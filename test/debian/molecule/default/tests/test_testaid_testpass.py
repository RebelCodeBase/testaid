import pytest
import testaid

testinfra_hosts = testaid.hosts()

# this test is xfailed by default
# as it assumes that you have done
# pass insert my_secret_key
# with password: my_secret_value
# FIXME: create mock
@pytest.mark.xfail
def test_testaid_debug(host, testvars, testpass):
    my_secret_value = testpass('my_secret_key')
    assert my_secret_value == 'my_secret_value'
