import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_system_whitelist(host, testvars):
    assert testvars['my_role_defaults_var'] == 'my_role_defaults_value'