import pytest
import shutil
import testaid


def test_testaid_moleculeenv_get_roles(moleculeplay, monkeypatch):
    base_dir = moleculeplay._moleculeenv._molecule_ephemeral_directory
    dir = base_dir / 'pytest_my_roles'
    dir.mkdir()
    roles_dir = dir / 'roles'
    roles_dir.mkdir()
    my_role_1 = roles_dir / 'my_role_1'
    my_role_1.mkdir()
    my_role_2 = roles_dir / 'my_role_2'
    my_role_2.mkdir()
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        '_get_project_dir_',
                        lambda x: dir)
    roles = moleculeplay._moleculeenv.get_roles()
    shutil.rmtree(dir)
    assert roles == ['my_role_1', 'my_role_2']

@pytest.mark.debug
def test_testaid_moleculeenv_create_symlinks(moleculeplay, monkeypatch):
    base_dir = moleculeplay._moleculeenv._molecule_ephemeral_directory
    dir = base_dir / 'pytest_my_symlinks'
    dir.mkdir()
    med = dir / 'molecule_ephemeral_directory'
    med.mkdir()
    roles_dir = dir / 'roles'
    roles_dir.mkdir()
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        'get_molecule_ephemeral_directory',
                        lambda x: med)
    monkeypatch.setattr(testaid.moleculeenv.MoleculeEnv,
                        '_get_project_dir_',
                        lambda x: dir)
    moleculeplay._moleculeenv._create_symlink_('roles')
    assert (med / 'roles').is_symlink()
    shutil.rmtree(dir)
