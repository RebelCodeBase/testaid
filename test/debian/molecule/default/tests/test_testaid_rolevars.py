import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_ymlfiles_second_role_default(testvars):
    assert testvars['my_vars_var1'] == 'vars_var1_content'
