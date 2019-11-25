import testaid

testinfra_hosts = testaid.hosts()


# issue: https://github.com/RebelCodeBase/testaid/issues/1
def test_testaid_system_github_issues_1(host, testvars):
    assert testvars['project_github_issues_1_file'] == 'bar'
