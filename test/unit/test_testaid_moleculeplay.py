def test_testaid_moleculeplay_is_not_none(moleculeplay):
    assert moleculeplay is not None


def test_testaid_moleculeplay_get_host(moleculeplay):
    assert moleculeplay.get_host() == moleculeplay._host
