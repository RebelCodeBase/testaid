import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_system_role_inventory(host, testvars):
    assert testvars['anarchism_group_vars_all'] == 'my_group_vars_value'
