import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_ruby_role_curl_install_packages_installed(host, testvars):
    curl_packages = testvars['curl_packages']
    for debian_package in curl_packages:
        deb = host.package(debian_package)
        assert deb.is_installed
