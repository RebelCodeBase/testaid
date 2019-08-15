import pytest
from testaid.exceptions import AnsibleRunError


def test_testaid_unit_moleculeplay_is_not_none(moleculeplay):
    assert moleculeplay is not None


def test_testaid_unit_moleculeplay_get_host(moleculeplay):
    assert moleculeplay.get_host() == moleculeplay._host


def test_testaid_unit_moleculeplay_exception_moleculeplayrunfailed_no_debug():
    result = ['my_result']
    msg = 'my_msg'
    with pytest.raises(AnsibleRunError) as excinfo:
        raise AnsibleRunError(result, msg)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'my_msg'


def test_testaid_unit_moleculeplay_exception_moleculeplayrunfailed_debug():
    result = ['my_result']
    msg = 'my_msg'
    with pytest.raises(AnsibleRunError) as excinfo:
        raise AnsibleRunError(result, msg, debug=True)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'my_msg\n\n[\n    "my_result"\n]'


def test_testaid_unit_moleculeplay_run_playbook_minimal(moleculeplay):
    playbook_minimal = \
        {'name': 'ansible minimal playbook',
         'hosts': 'localhost',
         'gather_facts': 'False'}
    result = moleculeplay.run_playbook(playbook_minimal)
    assert result == []
