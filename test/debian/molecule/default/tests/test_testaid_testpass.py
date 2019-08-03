import pytest
import testaid

testinfra_hosts = testaid.hosts()

# this test is skipped by default
# as it assumes that you have done
# pass insert my_secret_key
# with password: my_secret_value
@pytest.mark.skip
def test_testaid_debug(host, testvars, testpass):
    my_secret_value = testpass('my_secret_key')
    assert my_secret_value == 'my_secret_value'
