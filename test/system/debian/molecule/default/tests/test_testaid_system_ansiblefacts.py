import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_system_ansiblefacts_present(host, testvars, gather_localhost):
    if not gather_localhost:
        assert 'ansible_distribution_version' in testvars['ansible_facts']
