import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_ansiblefacts_present(host, testvars):
    assert 'ansible_distribution_version' in testvars['ansible_facts']
