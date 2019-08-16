import pytest
import testaid

testinfra_hosts = testaid.hosts()


@pytest.mark.debug
def test_testaid_system_role_packages_installed(host, testvars):
    assert 'anarchism_install' in testvars
    anarchism_packages = testvars['anarchism_packages']
    for debian_package in anarchism_packages:
        deb = host.package(debian_package)
        assert deb.is_installed
