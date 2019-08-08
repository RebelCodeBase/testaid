import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_varsfiles_role_vars(host, testvars):
    assert testvars['my_role_var'] == 'my_role_value'


def test_testaid_varsfiles_role_vars(host, testvars):
    assert testvars['my_project_var'] == 'my_project_value2'


def test_testaid_varsfiles_role_vars(host, testvars):
    assert testvars['my_extra_var'] == 'my_extra_value'


def test_testaid_varsfiles_role_vars(host, testvars):
    assert testvars['my_second_extra_var'] == 'my_second_extra_value'


def test_testaid_varsfiles_role_vars(host, testvars):
    assert testvars['my_custom_var'] == 'my_custom_value'
