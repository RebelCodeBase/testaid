def test_testaid_moleculeplay_is_not_none(moleculeplay):
    assert moleculeplay is not None


def test_testaid_moleculeplay_get_host(moleculeplay):
    assert moleculeplay.get_host() == moleculeplay._host


def test_testaid_moleculeplay_run_playbook_minimal(moleculeplay):
    playbook_minimal = \
        {'name': 'ansible minimal playbook',
         'hosts': 'localhost',
         'gather_facts': 'False'}
    result = moleculeplay.run_playbook(playbook_minimal)
    assert result == []
