from pathlib import Path


class MoleculeEnv(object):

    def __init__(self,
                 molecule_ephemeral_directory,
                 molecule_scenario_directory):

        self._molecule_ephemeral_directory = molecule_ephemeral_directory
        self._molecule_scenario_directory = molecule_scenario_directory

        # create symlink in molecule ephemeral directory
        # to roles directory in project dir
        self._create_symlink_('roles')

    def get_molecule_ephemeral_directory(self):
        return self._molecule_ephemeral_directory

    def get_molecule_scenario_directory(self):
        return self._molecule_scenario_directory

    def get_roles(self):
        '''Return roles as list of pathlib.Path objects'''
        project_dir = self._get_project_dir_()
        if project_dir is None:
            return list()
        roles_dir = project_dir / 'roles'
        roles = [d.name for d in roles_dir.iterdir() if d.is_dir()]
        return roles

    def _create_symlink_(self, path):
        '''Create symlink from molecule ephemeral dir to project dir.'''
        project_dir = self._get_project_dir_()
        if project_dir is None:
            return
        source = project_dir / path
        target = self.get_molecule_ephemeral_directory() / path
        try:
            target.symlink_to(source)
        except FileExistsError:
            pass

    def _get_project_dir_(self):
        '''Return ansible project dir.'''

        # start the ansible scenario directory
        path = self._molecule_scenario_directory

        # go up until you find the roles dir
        while path != Path('/'):
            path = path.parent
            if path / 'roles' in [d for d in path.iterdir() if d.is_dir()]:
                return path

        # else return None
        return None
