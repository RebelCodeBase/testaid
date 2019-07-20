import re
import testaid

testinfra_hosts = testaid.hosts()


def test_anarchism_fortune_greeting(host, testvars):
    if 'fortune-anarchism' in testvars['anarchism_packages']:
        with host.sudo():
            output = host.check_output('. /root/.bashrc')

            assert '---+-' in output