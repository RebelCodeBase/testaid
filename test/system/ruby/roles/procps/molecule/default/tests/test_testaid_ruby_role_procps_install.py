import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_ruby_role_procps_install_packages_installed(host, testvars):
    procps_packages = testvars['procps_packages']
    for debian_package in procps_packages:
        deb = host.package(debian_package)
        assert deb.is_installed
