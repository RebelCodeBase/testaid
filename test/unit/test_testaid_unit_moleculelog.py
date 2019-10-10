from testaid.moleculelog import MoleculeLog


def test_testaid_unit_moleculelog_is_not_none(moleculelog):
    assert moleculelog is not None


def test_testaid_unit_moleculelog_debug():
    moleculelog = MoleculeLog()
    moleculelog.debug('test message')
    log = moleculelog.get_log()
    assert log == 'test message\n'
