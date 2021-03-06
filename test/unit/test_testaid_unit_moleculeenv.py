from pathlib import Path
import testaid
from testaid.moleculeenv import MoleculeEnv


def test_testaid_unit_moleculeenv_is_not_none(moleculeenv):
    assert moleculeenv is not None
    assert moleculeenv.get_roles() == list()


def test_testaid_unit_moleculeenv_get_molecule_ephemeral_directory(
        moleculeenv,
        monkeypatch):
    med = moleculeenv.get_molecule_ephemeral_directory()
    assert med == moleculeenv._molecule_ephemeral_directory


def test_testaid_unit_moleculeenv_get_molecule_scenario_directory(
        moleculeenv,
        monkeypatch):
    msd = moleculeenv.get_molecule_scenario_directory()
    assert msd == moleculeenv._molecule_scenario_directory


def test_testaid_unit_moleculeenv_get_roles(
        moleculeenv,
        monkeypatch,
        tmp_path):
    my_roles = ['my_role_1', 'my_role_2']
    roles_dir = tmp_path / 'roles'
    roles_dir.mkdir()
    my_role_1 = roles_dir / 'my_role_1'
    my_role_1.mkdir()
    my_role_2 = roles_dir / 'my_role_2'
    my_role_2.mkdir()
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        'get_molecule_ephemeral_directory',
                        lambda x: tmp_path)
    roles = moleculeenv.get_roles()
    assert roles == my_roles


def test_testaid_unit_moleculeenv_create_symlinks(
        moleculeenv,
        monkeypatch,
        tmp_path):
    med = tmp_path / 'molecule_ephemeral_directory'
    med.mkdir()
    roles_dir = tmp_path / 'roles'
    roles_dir.mkdir()
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        'get_molecule_ephemeral_directory',
                        lambda x: med)
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        'get_project_dir',
                        lambda x: tmp_path)
    moleculeenv._create_symlink_('roles')
    assert (med / 'roles').is_symlink()


def test_testaid_unit_moleculeenv_create_symlinks_fileexistserror(
        moleculeenv,
        monkeypatch,
        tmp_path):
    med = tmp_path / 'molecule_ephemeral_directory'
    med.mkdir()
    roles_dir = tmp_path / 'roles'
    roles_dir.mkdir()
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        'get_molecule_ephemeral_directory',
                        lambda x: med)
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        'get_project_dir',
                        lambda x: tmp_path)

    # create symlink twice
    moleculeenv._create_symlink_('roles')
    moleculeenv._create_symlink_('roles')
    assert (med / 'roles').is_symlink()


def test_testaid_unit_moleculeenv_get_project_dir(
        moleculeenv,
        monkeypatch,
        tmp_path):
    msd = tmp_path / 'roles/my_role/molecule/default'
    msd.mkdir(parents=True)
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        'get_molecule_scenario_directory',
                        lambda x: msd)
    project_dir = moleculeenv.get_project_dir()
    assert project_dir == tmp_path


def test_testaid_unit_moleculeenv_get_project_dir_no_roles_dir(
        moleculeenv,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        'get_molecule_scenario_directory',
                        lambda x: Path('/'))
    project_dir = moleculeenv.get_project_dir()
    assert project_dir is None


def test_testaid_unit_moleculeenv_no_gather_roles(
        moleculelog,
        tmp_path):
    my_playbook = """\
---
- name: converge
  hosts: all
  gather_facts: false
  roles:
    - my_role
"""
    med = tmp_path / 'molecule_ephemeral_directory'
    med.mkdir()

    msd = tmp_path / 'molecule_scenario_directory'
    msd.mkdir()

    (tmp_path / 'roles' / 'my_role').mkdir(parents=True)

    playbook_path = msd / 'playbook.yml'
    playbook_path.write_text(my_playbook)

    gather_roles = False
    testvars_roles_blacklist = []
    testvars_roles_whitelist = []

    moleculeenv = MoleculeEnv(moleculelog,
                              med,
                              msd,
                              gather_roles,
                              testvars_roles_blacklist,
                              testvars_roles_whitelist)

    assert moleculeenv.get_roles() == []


def test_testaid_unit_moleculeenv_roles_from_custom_converge_playboook(
        moleculelog,
        tmp_path):
    my_molecule_yml = """\
---
provisioner:
    name: ansible
    playbooks:
        converge: my_playbook.yml
"""
    my_playbook = """\
---
- name: converge
  hosts: all
  gather_facts: false
  roles:
    - my_role
"""
    med = tmp_path / 'molecule_ephemeral_directory'
    med.mkdir()

    msd = tmp_path / 'molecule_scenario_directory'
    msd.mkdir()

    (tmp_path / 'roles' / 'my_role').mkdir(parents=True)

    molecule_yml_path = msd / 'molecule.yml'
    molecule_yml_path.write_text(my_molecule_yml)

    playbook_path = msd / 'my_playbook.yml'
    playbook_path.write_text(my_playbook)

    gather_roles = True
    testvars_roles_blacklist = []
    testvars_roles_whitelist = []

    moleculeenv = MoleculeEnv(moleculelog,
                              med,
                              msd,
                              gather_roles,
                              testvars_roles_blacklist,
                              testvars_roles_whitelist)

    assert moleculeenv.get_roles() == ['my_role']


def test_testaid_unit_moleculeenv_roles_from_default_converge_playboook(
        moleculelog,
        tmp_path):
    my_playbook = """\
---
- name: converge
  hosts: all
  gather_facts: false
  roles:
    - my_role
"""
    med = tmp_path / 'molecule_ephemeral_directory'
    med.mkdir()

    msd = tmp_path / 'molecule_scenario_directory'
    msd.mkdir()

    (tmp_path / 'roles' / 'my_role').mkdir(parents=True)

    playbook_path = msd / 'playbook.yml'
    playbook_path.write_text(my_playbook)

    gather_roles = True
    testvars_roles_blacklist = []
    testvars_roles_whitelist = []

    moleculeenv = MoleculeEnv(moleculelog,
                              med,
                              msd,
                              gather_roles,
                              testvars_roles_blacklist,
                              testvars_roles_whitelist)

    assert moleculeenv.get_roles() == ['my_role']


def test_testaid_unit_moleculeenv_get_roles_not_blacklisted(
        moleculelog,
        tmp_path):
    my_playbook = """\
---
- name: converge
  hosts: all
  gather_facts: false
  roles:
    - my_role_1
    - my_role_2
"""
    my_roles = ['my_role_2']

    med = tmp_path / 'molecule_ephemeral_directory'
    med.mkdir()

    msd = tmp_path / 'molecule_scenario_directory'
    msd.mkdir()

    my_role_1 = tmp_path / 'roles' / 'my_role_1'
    my_role_1.mkdir(parents=True)

    my_role_2 = tmp_path / 'roles' / 'my_role_2'
    my_role_2.mkdir()

    playbook_path = msd / 'playbook.yml'
    playbook_path.write_text(my_playbook)

    gather_roles = True
    testvars_roles_blacklist = ['my_role_1']
    testvars_roles_whitelist = []

    moleculeenv = MoleculeEnv(moleculelog,
                              med,
                              msd,
                              gather_roles,
                              testvars_roles_blacklist,
                              testvars_roles_whitelist)

    assert moleculeenv.get_roles() == my_roles


def test_testaid_unit_moleculeenv_get_roles_whitelisted(
        moleculelog,
        tmp_path):
    my_playbook = """\
---
- name: converge
  hosts: all
  gather_facts: false
  roles:
    - my_role_1
    - my_role_2
"""
    my_roles = ['my_role_2']

    med = tmp_path / 'molecule_ephemeral_directory'
    med.mkdir()

    msd = tmp_path / 'molecule_scenario_directory'
    msd.mkdir()

    my_role_1 = tmp_path / 'roles' / 'my_role_1'
    my_role_1.mkdir(parents=True)

    my_role_2 = tmp_path / 'roles' / 'my_role_2'
    my_role_2.mkdir()

    playbook_path = msd / 'playbook.yml'
    playbook_path.write_text(my_playbook)

    gather_roles = True
    testvars_roles_blacklist = []
    testvars_roles_whitelist = ['my_role_2']

    moleculeenv = MoleculeEnv(moleculelog,
                              med,
                              msd,
                              gather_roles,
                              testvars_roles_blacklist,
                              testvars_roles_whitelist)

    assert moleculeenv.get_roles() == my_roles


def test_testaid_unit_moleculeenv_vars_config_molecule_yml(
        moleculelog,
        tmp_path):
    med = tmp_path / 'molecule_ephemeral_directory'
    med.mkdir()

    msd = tmp_path / 'molecule_scenario_directory'
    msd.mkdir()

    gather_roles = True
    testvars_roles_blacklist = []
    testvars_roles_whitelist = []

    moleculeenv = MoleculeEnv(moleculelog,
                              med,
                              msd,
                              gather_roles,
                              testvars_roles_blacklist,
                              testvars_roles_whitelist)

    expected_config = 'Using variables defined in ' + str(msd / 'molecule.yml')
    molecule_vars_config = moleculeenv._get_molecule_vars_config_()
    assert molecule_vars_config == expected_config


def test_testaid_unit_moleculeenv_vars_config_group_vars(
        moleculelog,
        tmp_path):
    med = tmp_path / 'molecule_ephemeral_directory'
    med.mkdir()

    msd = tmp_path / 'molecule_scenario_directory'
    msd.mkdir()

    group_vars_target = msd / 'group_vars'
    group_vars_target.mkdir()

    inventory_dir = med / 'inventory'
    inventory_dir.mkdir()

    group_vars = inventory_dir / 'group_vars'
    group_vars.symlink_to(group_vars_target, target_is_directory=True)

    gather_roles = True
    testvars_roles_blacklist = []
    testvars_roles_whitelist = []

    moleculeenv = MoleculeEnv(moleculelog,
                              med,
                              msd,
                              gather_roles,
                              testvars_roles_blacklist,
                              testvars_roles_whitelist)

    expected_config = 'Using group_vars symlink to ' + str(group_vars_target)
    molecule_vars_config = moleculeenv._get_molecule_vars_config_()
    assert molecule_vars_config == expected_config


def test_testaid_unit_moleculeenv_vars_config_host_vars(
        moleculelog,
        tmp_path):
    med = tmp_path / 'molecule_ephemeral_directory'
    med.mkdir()

    msd = tmp_path / 'molecule_scenario_directory'
    msd.mkdir()

    host_vars_target = msd / 'host_vars'
    host_vars_target.mkdir()

    inventory_dir = med / 'inventory'
    inventory_dir.mkdir()

    host_vars = inventory_dir / 'host_vars'
    host_vars.symlink_to(host_vars_target, target_is_directory=True)

    gather_roles = True
    testvars_roles_blacklist = []
    testvars_roles_whitelist = []

    moleculeenv = MoleculeEnv(moleculelog,
                              med,
                              msd,
                              gather_roles,
                              testvars_roles_blacklist,
                              testvars_roles_whitelist)

    expected_config = 'Using host_vars symlink to ' + str(host_vars_target)
    molecule_vars_config = moleculeenv._get_molecule_vars_config_()
    assert molecule_vars_config == expected_config


def test_testaid_unit_moleculeenv_vars_config_host_vars_and_group_vars(
        moleculelog,
        tmp_path):
    med = tmp_path / 'molecule_ephemeral_directory'
    med.mkdir()

    msd = tmp_path / 'molecule_scenario_directory'
    msd.mkdir()

    group_vars_target = msd / 'group_vars'
    group_vars_target.mkdir()

    host_vars_target = msd / 'host_vars'
    host_vars_target.mkdir()

    inventory_dir = med / 'inventory'
    inventory_dir.mkdir()

    group_vars = inventory_dir / 'group_vars'
    group_vars.symlink_to(group_vars_target, target_is_directory=True)

    host_vars = inventory_dir / 'host_vars'
    host_vars.symlink_to(host_vars_target, target_is_directory=True)

    gather_roles = True
    testvars_roles_blacklist = []
    testvars_roles_whitelist = []

    moleculeenv = MoleculeEnv(moleculelog,
                              med,
                              msd,
                              gather_roles,
                              testvars_roles_blacklist,
                              testvars_roles_whitelist)

    expected_config = 'Using group_vars symlink to ' + str(group_vars_target)
    expected_config += '\n'
    expected_config += 'Using host_vars symlink to ' + str(host_vars_target)
    molecule_vars_config = moleculeenv._get_molecule_vars_config_()
    assert molecule_vars_config == expected_config
