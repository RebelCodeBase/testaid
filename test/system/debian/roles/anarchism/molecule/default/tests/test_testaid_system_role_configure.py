import re
import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_system_role_fortune_configures(host, testvars):
    if 'fortune-anarchism' in testvars['anarchism_packages']:
        with host.sudo():
            file = host.file('/root/.bashrc')
            expected = '''
echo
/usr/games/fortune -s anarchism
echo
'''
            assert re.search(expected, file.content_string) is not None
