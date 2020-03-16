import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_system_project_group(host, testvars):
    assert testvars['anarchism_group_vars_private'] == 'my_group_vars_private_value'
