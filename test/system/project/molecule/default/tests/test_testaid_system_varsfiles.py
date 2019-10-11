import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_system_varsfiles_role_defaults(host, testvars):
    assert testvars['my_role_defaults_var'] == 'my_role_defaults_value'


def test_testaid_system_varsfiles_role_vars(host, testvars):
    assert testvars['my_role_var'] == 'my_role_value'


def test_testaid_system_varsfiles_project_vars(host, testvars):
    assert testvars['my_project_var'] == 'my_project_value'


def test_testaid_system_varsfiles_extra_vars(host, testvars):
    assert testvars['my_extra_var'] == 'my_extra_value'


def test_testaid_system_varsfiles_second_file_in_vars_dir(host, testvars):
    assert testvars['my_custom_var'] == 'my_custom_value'
