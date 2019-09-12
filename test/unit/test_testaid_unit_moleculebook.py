import pytest
import testaid
from testaid.exceptions import MoleculeBookRunError


def test_testaid_unit_moleculebook_is_not_none(moleculebook):
    assert moleculebook is not None


def test_testaid_unit_moleculebook_get(moleculebook):
    assert moleculebook.get() == moleculebook._playbook


def test_testaid_unit_moleculebook_set(moleculebook):
    playbook = "\n---\n- name: localplay\n  hosts: localhost"
    moleculebook.set(playbook)
    assert moleculebook._playbook == playbook


def test_testaid_unit_moleculebook_create_default(moleculebook):
    playbook_default = \
        {'name': 'ansible playbook',
         'hosts': 'localhost',
         'gather_facts': 'True',
         'vars_files': [],
         'roles': [],
         'tasks': []}
    moleculebook.create()
    playbook = moleculebook._playbook
    assert playbook == playbook_default


def test_testaid_unit_moleculebook_create_extra_vars(
        moleculebook,
        monkeypatch):
    playbook_extra_vars = \
        {'name': 'ansible playbook',
         'hosts': 'localhost',
         'gather_facts': 'True',
         'vars_files': ['my_extra_vars.yml'],
         'roles': [],
         'tasks': []}
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        '_get_extra_vars_files_',
                        lambda x: ['my_extra_vars.yml'])
    moleculebook.create(extra_vars=True)
    playbook = moleculebook._playbook
    assert playbook == playbook_extra_vars


def test_testaid_unit_moleculebook_create_gather_roles(
        moleculebook,
        monkeypatch):
    playbook_roles = \
        {'name': 'ansible playbook',
         'hosts': 'localhost',
         'gather_facts': 'True',
         'vars_files': [],
         'roles': [{'name': 'my_role', 'when': 'False'}],
         'tasks': []}
    monkeypatch.setattr(testaid.moleculeplay.MoleculePlay,
                        'get_roles',
                        lambda x: ['my_role'])
    moleculebook.create(gather_roles=True)
    playbook = moleculebook._playbook
    assert playbook == playbook_roles


def test_testaid_unit_moleculebook_add_task_debug(moleculebook):
    playbook_task_debug = \
        {'name': 'ansible playbook',
         'hosts': 'localhost',
         'gather_facts': 'True',
         'vars_files': [],
         'roles': [],
         'tasks': [{'action': {'module': 'debug',
                               'args': {'msg': 'Happy testing!'}}}]}
    moleculebook.create()
    moleculebook.add_task_debug("Happy testing!")
    playbook = moleculebook._playbook
    assert playbook == playbook_task_debug


def test_testaid_unit_moleculebook_add_task_include_vars_dir(moleculebook):
    playbook_task_debug = \
        {'name': 'ansible playbook',
         'hosts': 'localhost',
         'gather_facts': 'True',
         'vars_files': [],
         'roles': [],
         'tasks': [{'action': {'module': 'include_vars',
                               'args': {'dir': 'my_custom_vars'}}}]}
    moleculebook.create()
    moleculebook.add_task_include_vars_dir("my_custom_vars")
    playbook = moleculebook._playbook
    assert playbook == playbook_task_debug


def test_testaid_unit_moleculebook_run(moleculebook, monkeypatch):
    monkeypatch.setattr(testaid.moleculeplay.MoleculePlay,
                        'run_playbook',
                        lambda x, y: 'my_playbook_result')
    playbook_result = moleculebook.run()
    assert playbook_result == 'my_playbook_result'


def test_testaid_unit_moleculebook_get_vars_default(moleculebook):
    vars = moleculebook.get_vars()
    assert 'inventory_file' in vars


def test_testaid_unit_moleculebook_get_vars_no_run_playbook(moleculebook):
    vars = moleculebook.get_vars(run_playbook=False)
    assert 'inventory_hostname' in vars


def test_testaid_unit_moleculebook_get_vars_gather_facts(moleculebook):
    vars = moleculebook.get_vars(gather_facts=True)
    assert 'ansible_facts' in vars


def test_testaid_unit_moleculebook_get_vars_no_gather_facts(moleculebook):
    vars = moleculebook.get_vars(gather_facts=False)
    assert 'inventory_file' in vars


def test_testaid_unit_moleculebook_get_vars_gather_facts_index_error(
        moleculebook,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'run',
                        lambda x: [])
    with pytest.raises(MoleculeBookRunError) as excinfo:
        moleculebook.get_vars()
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Unable to gather ansible vars and facts.'


def test_testaid_unit_moleculebook_get_vars_gather_facts_key_error(
        moleculebook,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'run',
                        lambda x: [{}, {}])
    with pytest.raises(MoleculeBookRunError) as excinfo:
        moleculebook.get_vars()
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Unable to gather ansible vars and facts.'


def test_testaid_unit_moleculebook_get_vars_no_gather_facts_index_error(
        moleculebook,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'run',
                        lambda x: [])
    with pytest.raises(
            MoleculeBookRunError,
            match=r'Unable to gather ansible vars\..*'):
        moleculebook.get_vars(gather_facts=False)


def test_testaid_unit_moleculebook_get_vars_no_gather_facts_key_error(
        moleculebook,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'run',
                        lambda x: [{}, {}])
    with pytest.raises(
            MoleculeBookRunError,
            match=r'Unable to gather ansible vars\..*'):
        moleculebook.get_vars(gather_facts=False)


def test_testaid_unit_moleculebook_exception_moleculebookrunerror_no_debug():
    result = ['my_result']
    msg = 'my_msg'
    with pytest.raises(MoleculeBookRunError) as excinfo:
        raise MoleculeBookRunError(result, msg)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'my_msg'


def test_testaid_unit_moleculebook_exception_moleculebookrunerror_debug():
    result = ['my_result']
    msg = 'my_msg'
    with pytest.raises(MoleculeBookRunError) as excinfo:
        raise MoleculeBookRunError(result, msg, debug=True)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'my_msg\n\n[\n    "my_result"\n]'


def test_testaid_unit_get_molecule_scenario_directory(moleculebook):
    moleculeplay_mcd = \
        moleculebook._moleculeplay.get_molecule_scenario_directory()
    moleculebook_mcd = \
        moleculebook._get_molecule_scenario_directory_()
    assert moleculebook_mcd == moleculeplay_mcd


def test_testaid_unit_moleculebook_extra_vars_files_no_files(moleculebook):
    files = moleculebook._extra_vars_files_()
    assert files == []


def test_testaid_unit_moleculebook_extra_vars_files_file(
        moleculebook,
        monkeypatch,
        tmp_path):
    filename = 'my_extra_vars.yml'
    filepath = 'pytest_my_extra_vars/' + filename
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        '_get_extra_vars_',
                        lambda x: filepath)
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        '_get_molecule_scenario_directory_',
                        lambda x: tmp_path)
    dir = tmp_path / 'pytest_my_extra_vars'
    dir.mkdir()
    file = dir / filename
    file.touch()
    files = moleculebook._extra_vars_files_()
    assert files == [file]


def test_testaid_unit_moleculebook_extra_vars_files_dir_one_file(
        moleculebook,
        monkeypatch,
        tmp_path):
    filename = 'my_extra_vars.yml'
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        '_get_extra_vars_',
                        lambda x: 'pytest_my_extra_vars')
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        '_get_molecule_scenario_directory_',
                        lambda x: tmp_path)
    dir = tmp_path / 'pytest_my_extra_vars'
    dir.mkdir()
    file = dir / filename
    file.touch()
    files = moleculebook._extra_vars_files_()
    assert files == [file]


def test_testaid_unit_moleculebook_extra_vars_files_dir_two_files(
        moleculebook,
        monkeypatch,
        tmp_path):
    filename1 = 'my_extra_vars_1.yml'
    filename2 = 'my_extra_vars_2.yml'
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        '_get_extra_vars_',
                        lambda x: 'pytest_my_extra_vars')
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        '_get_molecule_scenario_directory_',
                        lambda x: tmp_path)
    dir = tmp_path / 'pytest_my_extra_vars'
    dir.mkdir()
    file1 = dir / filename1
    file1.touch()
    file2 = dir / filename2
    file2.touch()
    files = moleculebook._extra_vars_files_()
    assert files == [file1, file2]
