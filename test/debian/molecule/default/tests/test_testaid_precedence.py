import os
import re
import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_precedence_can_read_role_default(testvars):
    assert testvars['anarchism_install']


def test_testaid_precedence_project_beats_role_default(testvars):
    expected = ['anarchism', 'fortune-anarchism']

    assert testvars['anarchism_packages'] == expected
