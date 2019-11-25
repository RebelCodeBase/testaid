import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_system_role_system_fortune_greeting(host, testvars):
    if 'fortune-anarchism' in testvars['anarchism_packages']:
        with host.sudo():
            output = host.check_output('. /root/.bashrc')
            assert '---+-' in output
