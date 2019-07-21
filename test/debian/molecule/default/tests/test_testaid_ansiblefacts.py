import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_ansiblefacts_present(testvars):
    assert 'ansible_all_ipv4_addresses' in testvars['ansible_facts'].keys()
