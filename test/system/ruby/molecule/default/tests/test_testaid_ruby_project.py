import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_ruby_project_test_ruby(host):
    assert host.run('ruby')
