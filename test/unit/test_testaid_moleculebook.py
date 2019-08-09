import testaid
import json

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
                        lambda x: ['my_extra_vars.yml'])
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
