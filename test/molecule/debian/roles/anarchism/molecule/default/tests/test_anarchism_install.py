import testaid

testinfra_hosts = testaid.hosts()


def test_anarchism_packages_installed(host, testvars):
    if testvars['anarchism_install']:
        anarchism_packages = testvars['anarchism_packages']

        for debian_package in anarchism_packages:
            deb = host.package(debian_package)

            assert deb.is_installed
