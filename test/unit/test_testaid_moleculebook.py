import pytest
import shutil
import testaid
from testaid.exceptions import MoleculeBookRunFailed


def test_testaid_moleculebook_is_not_none(moleculebook):
    assert moleculebook is not None


def test_testaid_moleculebook_get(moleculebook):
    assert moleculebook.get() == moleculebook._playbook


def test_testaid_moleculebook_set(moleculebook):
    playbook = "\n---\n- name: localplay\n  hosts: localhost"
    moleculebook.set(playbook)
    assert moleculebook._playbook == playbook


def test_testaid_moleculebook_create_default(moleculebook):
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


def test_testaid_moleculebook_create_extra_vars(moleculebook, monkeypatch):
    playbook_extra_vars = \
        {'name': 'ansible playbook',
         'hosts': 'localhost',
         'gather_facts': 'True',
         'vars_files': ['my_extra_vars.yml'],
         'roles': [],
         'tasks': []}
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        '_extra_vars_files_',
                        lambda x, y: ['my_extra_vars.yml'])
    moleculebook.create(extra_vars=True)
    playbook = moleculebook._playbook
    assert playbook == playbook_extra_vars


def test_testaid_moleculebook_create_gather_roles(moleculebook, monkeypatch):
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


def test_testaid_moleculebook_add_task_debug(moleculebook):
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


def test_testaid_moleculebook_add_task_include_vars_dir(moleculebook):
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


def test_testaid_moleculebook_run(moleculebook, monkeypatch):
    monkeypatch.setattr(testaid.moleculeplay.MoleculePlay,
                        'run_playbook',
                        lambda x, y: 'my_playbook_result')
    playbook_result = moleculebook.run()
    assert playbook_result == 'my_playbook_result'


def test_testaid_moleculebook_get_vars_default(moleculebook):
    vars = moleculebook.get_vars()
    assert 'inventory_file' in vars


def test_testaid_moleculebook_get_vars_no_run_playbook(moleculebook):
    vars = moleculebook.get_vars(run_playbook=False)
    assert 'inventory_hostname' in vars


def test_testaid_moleculebook_get_vars_gather_facts(moleculebook):
    vars = moleculebook.get_vars(gather_facts=True)
    assert 'ansible_facts' in vars


def test_testaid_moleculebook_get_vars_no_gather_facts(moleculebook):
    vars = moleculebook.get_vars(gather_facts=False)
    assert 'inventory_file' in vars


def test_testaid_moleculebook_get_vars_gather_facts_index_error(
        moleculebook,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'run',
                        lambda x: [])
    with pytest.raises(
            MoleculeBookRunFailed,
            match=r'Unable to gather ansible vars and facts\..*'):
        moleculebook.get_vars()


def test_testaid_moleculebook_get_vars_gather_facts_key_error(
        moleculebook,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'run',
                        lambda x: [{}, {}])
    with pytest.raises(
            MoleculeBookRunFailed,
            match=r'Unable to gather ansible vars and facts\..*'):
        moleculebook.get_vars()


def test_testaid_moleculebook_get_vars_no_gather_facts_index_error(
        moleculebook,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'run',
                        lambda x: [])
    with pytest.raises(
            MoleculeBookRunFailed,
            match=r'Unable to gather ansible vars\..*'):
        moleculebook.get_vars(gather_facts=False)


def test_testaid_moleculebook_get_vars_no_gather_facts_key_error(
        moleculebook,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'run',
                        lambda x: [{}, {}])
    with pytest.raises(
            MoleculeBookRunFailed,
            match=r'Unable to gather ansible vars\..*'):
        moleculebook.get_vars(gather_facts=False)


def test_testaid_moleculebook_exception_moleculebookrunfailed_no_debug():
    result = ['my_result']
    msg = 'my_msg'
    with pytest.raises(
            MoleculeBookRunFailed,
            match=r'^my_msg$'):
        raise MoleculeBookRunFailed(result, msg)


def test_testaid_moleculebook_exception_moleculebookrunfailed_debug():
    result = ['my_result']
    msg = 'my_msg'
    with pytest.raises(
            MoleculeBookRunFailed,
            match=r'.*my_result.*'):
        raise MoleculeBookRunFailed(result, msg, debug=True)


def test_testaid_moleculebook_extra_vars_files_no_files(
        moleculebook,
        monkeypatch):
    files = moleculebook._extra_vars_files_('')
    assert files == []


def test_testaid_moleculebook_extra_vars_files_file(
        moleculebook,
        monkeypatch):
    filename = 'my_extra_vars.yml'
    filepath = 'pytest_my_extra_vars/' + filename
    dir = moleculebook._molecule_scenario_directory / 'pytest_my_extra_vars'
    dir.mkdir()
    file = dir / filename
    file.touch()
    files = moleculebook._extra_vars_files_(filepath)
    shutil.rmtree(dir)
    assert files == [file]


def test_testaid_moleculebook_extra_vars_files_dir_one_file(
        moleculebook,
        monkeypatch):
    filename = 'my_extra_vars.yml'
    dir = moleculebook._molecule_scenario_directory / 'pytest_my_extra_vars'
    dir.mkdir()
    file = dir / filename
    file.touch()
    files = moleculebook._extra_vars_files_('pytest_my_extra_vars')
    shutil.rmtree(dir)
    assert files == [file]


def test_testaid_moleculebook_extra_vars_files_dir_two_files(
        moleculebook,
        monkeypatch):
    filename1 = 'my_extra_vars_1.yml'
    filename2 = 'my_extra_vars_2.yml'
    dir = moleculebook._molecule_scenario_directory / 'pytest_my_extra_vars'
    dir.mkdir()
    file1 = dir / filename1
    file1.touch()
    file2 = dir / filename2
    file2.touch()
    files = moleculebook._extra_vars_files_('pytest_my_extra_vars')
    shutil.rmtree(dir)
    assert files == [file2, file1]
