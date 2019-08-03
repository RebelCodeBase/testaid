import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_varsfiles_role_vars(host, testvars):
    assert testvars['my_role_var'] == 'role_var'
