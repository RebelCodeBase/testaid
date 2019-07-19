import testaid

testinfra_hosts = testaid.hosts()


def test_anarchism_packages_installed(host, testvars):
    anarchism_packages = testvars['anarchism_packages']

    for debian_package in anarchism_packages:
        deb = host.package(debian_package)

        assert deb.is_installed
