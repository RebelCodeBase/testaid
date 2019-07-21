import testaid

testinfra_hosts = testaid.hosts()

# issue: https://github.com/RebelCodeBase/testaid/issues/1
# needs: https://github.com/philpep/testinfra/pull/462
#def test_testaid_github_issues_1(testvars):
#    assert testvars['github_issues_1_file'] == 'bar'
