import testaid

testinfra_hosts = testaid.hosts()


def test_anarchism_inventory(host, testvars):
    assert testvars['group_vars_all'] == 'my_group_vars_value'
