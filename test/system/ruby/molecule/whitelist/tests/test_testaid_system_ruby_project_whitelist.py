import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_ruby_project_test_whitelist_curl_and_vim(host, testvars):
    assert 'curl_packages' in testvars
    assert 'vim_packages' in testvars
    assert 'gpg_packages' not in testvars
    assert 'procps_packages' not in testvars
