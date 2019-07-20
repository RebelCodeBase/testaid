import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_ymlfiles_role_vars(testvars):
    assert testvars['my_role_var'] == 'role_var'


def test_testaid_ymlfiles_project_vars(testvars):
    assert testvars['my_project_vars_main'] == 'project_vars_main'


def test_testaid_ymlfiles_project_multiple_vars_files(testvars):
    assert testvars['my_project_vars_second'] == 'project_vars_second'


def test_testaid_ymlfiles_extra_vars_files(testvars):
    assert testvars['my_extra_vars_first'] == 'extra_vars_first'
    assert testvars['my_extra_vars_second'] == 'extra_vars_second'
