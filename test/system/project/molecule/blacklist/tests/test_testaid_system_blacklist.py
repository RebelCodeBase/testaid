import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_system_blacklist(host, testvars):
    assert 'my_role_defaults_var' not in testvars
