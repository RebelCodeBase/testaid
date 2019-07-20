import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_ymlfiles_role_vars(testvars):
    assert testvars['my_vars_var1'] == 'vars_var1_content'


def test_testaid_ymlfiles_project_vars(testvars):
    assert testvars['my_project_vars_main'] == 'project_vars_main'


def test_testaid_ymlfiles_project_multiple_vars_files(testvars):
    assert testvars['my_project_vars_second'] == 'project_vars_second'
