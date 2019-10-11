import testaid
from testaid.moleculelog import MoleculeLog


def test_testaid_unit_moleculelog_is_not_none(moleculelog):
    assert moleculelog is not None


def test_testaid_unit_moleculelog_debug():
    moleculelog = MoleculeLog()
    moleculelog.debug('test message')
    log = moleculelog.get_log()
    assert log == 'test message\n'


def test_testaid_unit_moleculelog_print_debug_none(
        capsys,
        moleculelog,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculelog.MoleculeLog,
                        'get_log',
                        lambda x: '')
    expected_out = ''
    moleculelog.print_debug()
    captured = capsys.readouterr()
    assert captured.out == expected_out


def test_testaid_unit_moleculelog_print_debug_os(
        capsys,
        moleculelog,
        monkeypatch):
    monkeypatch.setenv('TESTVARS_TESTENV', 'testvalue')
    monkeypatch.setattr(testaid.moleculelog.MoleculeLog,
                        'get_log',
                        lambda x: '')
    expected_out = '\n\n' \
                   '\x1b[47m\x1b[1m\x1b[30m' \
                   'DEBUG: TESTVARS ENVIRONMENT' \
                   '\x1b[39m\x1b[49m\x1b[0m\n' \
                   '\x1b[30m\x1b[1m---\n' \
                   'TESTVARS_TESTENV: testvalue\n' \
                   '\x1b[0m\x1b[39m\n'
    moleculelog.print_debug()
    captured = capsys.readouterr()
    assert captured.out == expected_out


def test_testaid_unit_moleculelog_print_debug_log(
        capsys,
        moleculelog,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculelog.MoleculeLog,
                        'get_log',
                        lambda x: 'my_log_message\n')
    expected_out = '\n\n' \
                   '\x1b[47m\x1b[1m\x1b[30m' \
                   'DEBUG: TESTVARS LOG' \
                   '\x1b[39m\x1b[49m\x1b[0m\n' \
                   '\x1b[30m\x1b[1m' \
                   'my_log_message\n' \
                   '\x1b[0m\x1b[39m\n'
    moleculelog.print_debug()
    captured = capsys.readouterr()
    assert captured.out == expected_out


def test_testaid_unit_moleculelog_print_debug_os_and_log(
        capsys,
        moleculelog,
        monkeypatch):
    monkeypatch.setenv('TESTVARS_TESTENV', 'testvalue')
    monkeypatch.setattr(testaid.moleculelog.MoleculeLog,
                        'get_log',
                        lambda x: 'my_log_message\n')
    expected_out = '\n\n' \
                   '\x1b[47m\x1b[1m\x1b[30m' \
                   'DEBUG: TESTVARS ENVIRONMENT' \
                   '\x1b[39m\x1b[49m\x1b[0m\n\x1b[30m\x1b[1m' \
                   '---\n' \
                   'TESTVARS_TESTENV: testvalue\n' \
                   '\x1b[0m\x1b[39m\n\x1b[47m\x1b[1m\x1b[30m' \
                   'DEBUG: TESTVARS LOG' \
                   '\x1b[39m\x1b[49m\x1b[0m\n' \
                   '\x1b[30m\x1b[1m' \
                   'my_log_message\n' \
                   '\x1b[0m\x1b[39m\n'
    moleculelog.print_debug()
    captured = capsys.readouterr()
    assert captured.out == expected_out
