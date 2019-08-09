def test_testaid_moleculebook_is_not_none(moleculebook):
    assert moleculebook is not None


def test_testaid_moleculebook_get_playbook(moleculebook):
    assert moleculebook.get() == moleculebook._playbook


