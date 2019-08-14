import pytest
from testaid.exceptions import AnsibleRunFailed


def test_testaid_unit_moleculeplay_is_not_none(moleculeplay):
    assert moleculeplay is not None


def test_testaid_unit_moleculeplay_get_host(moleculeplay):
    assert moleculeplay.get_host() == moleculeplay._host


def test_testaid_unit_moleculeplay_exception_moleculeplayrunfailed_no_debug():
    result = ['my_result']
    msg = 'my_msg'
    with pytest.raises(
            AnsibleRunFailed,
            match=r'^my_msg$'):
        raise AnsibleRunFailed(result, msg)


def test_testaid_unit_moleculeplay_exception_moleculeplayrunfailed_debug():
    result = ['my_result']
    msg = 'my_msg'
    with pytest.raises(
            AnsibleRunFailed,
            match=r'.*my_result.*'):
        raise AnsibleRunFailed(result, msg, debug=True)


def test_testaid_unit_moleculeplay_run_playbook_minimal(moleculeplay):
    playbook_minimal = \
        {'name': 'ansible minimal playbook',
         'hosts': 'localhost',
         'gather_facts': 'False'}
    result = moleculeplay.run_playbook(playbook_minimal)
    assert result == []
