import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_ruby_role_vim_system(host):
    assert host.run('vim --version')
