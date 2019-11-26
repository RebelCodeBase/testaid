import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_ruby_role_curl_system(host):
    assert host.run('curl')
