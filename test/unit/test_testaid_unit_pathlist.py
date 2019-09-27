from pathlib import Path
from testaid.pathlist import PathList


def test_testaid_unit_pathlist_roles_blacklist(testvars_roles_blacklist):
    assert testvars_roles_blacklist is not None


def test_testaid_unit_pathlist_roles_whitelist(testvars_roles_whitelist):
    assert testvars_roles_whitelist is not None


def test_testaid_unit_pathlist_get(tmp_path):
    msd = tmp_path / 'molecule_scenario_directory'
    dir1 = msd / 'dir1'
    dir1.mkdir(parents=True)
    dir2 = tmp_path / 'dir2'
    dir2.mkdir()
    file1 = dir1 / 'file1.yml'
    file1.touch()
    file2 = dir1 / 'file2.yml'
    file2.touch()
    file3 = dir2 / 'file3.yml'
    file3.touch()
    my_pathlist = [Path(file3), Path(file1), Path(file2)]
    my_pathstring = 'dir1:../dir2/file3.yml'
    pathlist = PathList(my_pathstring, msd)
    assert pathlist.get() == my_pathlist
