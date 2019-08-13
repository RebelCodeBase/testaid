from pathlib import Path
import testaid


def test_testaid_moleculeenv_is_not_none(moleculeenv):
    assert moleculeenv is not None


def test_testaid_moleculeenv_get_molecule_ephemeral_directory(
        moleculeenv,
        monkeypatch):
    med = moleculeenv.get_molecule_ephemeral_directory()
    assert med == moleculeenv._molecule_ephemeral_directory


def test_testaid_moleculeenv_get_molecule_scenario_directory(
        moleculeenv,
        monkeypatch):
    msd = moleculeenv.get_molecule_scenario_directory()
    assert msd == moleculeenv._molecule_scenario_directory


def test_testaid_moleculeenv_get_roles(
        moleculeenv,
        monkeypatch,
        tmp_path):
    roles_dir = tmp_path / 'roles'
    roles_dir.mkdir()
    my_role_1 = roles_dir / 'my_role_1'
    my_role_1.mkdir()
    my_role_2 = roles_dir / 'my_role_2'
    my_role_2.mkdir()
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        'get_project_dir',
                        lambda x: tmp_path)
    roles = moleculeenv.get_roles()
    assert roles == ['my_role_1', 'my_role_2']


def test_testaid_moleculeenv_create_symlinks(
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


def test_testaid_moleculeenv_create_symlinks_fileexistserror(
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


def test_testaid_moleculeenv_get_project_dir(
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


def test_testaid_moleculeenv_get_project_dir_no_roles_dir(
        moleculeenv,
        monkeypatch):
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        'get_molecule_scenario_directory',
                        lambda x: Path('/'))
    project_dir = moleculeenv.get_project_dir()
    assert project_dir is None
