from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError


class MoleculeEnv(object):

    def __init__(self,
                 molecule_ephemeral_directory,
                 molecule_scenario_directory,
                 gather_roles,
                 testvars_roles_blacklist,
                 testvars_roles_whitelist):
        self._molecule_ephemeral_directory = molecule_ephemeral_directory
        self._molecule_scenario_directory = molecule_scenario_directory
        self._gather_roles = gather_roles
        self._testvars_roles_blacklist = testvars_roles_blacklist
        self._testvars_roles_whitelist = testvars_roles_whitelist
        self._configure_roles_()

    def get_molecule_ephemeral_directory(self):
        return self._molecule_ephemeral_directory

    def get_molecule_scenario_directory(self):
        return self._molecule_scenario_directory

    def get_project_dir(self):
        '''Return ansible project dir.'''

        # start the ansible scenario directory
        path = self.get_molecule_scenario_directory()

        # go up until you find the roles dir
        while path != Path('/'):
            path = path.parent
            if path / 'roles' in [d for d in path.iterdir() if d.is_dir()]:
                return path

        # else return None
        return None

    def get_roles(self):
        '''Return roles as list of pathlib.Path objects'''
        roles_dir = self.get_molecule_ephemeral_directory() / 'roles'

        if not roles_dir.exists():
            return list()

        roles = sorted([d.name for d in roles_dir.iterdir() if d.is_dir()])
        return roles

    def _configure_roles_(self):
        '''Create symlinks to roles'''
        if self._gather_roles is False:
            return

        roles = None

        if self._get_testvars_roles_whitelist_():
            roles = self._get_testvars_roles_whitelist_()

        # try to read roles from custom molecule converge playbook
        if roles is None:
            playbook_file = self._read_playbook_file_from_molecule_yml_()
            if playbook_file is not None:
                roles = self._read_roles_from_playbook_(playbook_file)

        # try to read roles from default molecule converge playbook
        if roles is None:
            roles = self._read_roles_from_playbook_('converge.yml')

        # if roles have been selected
        # then apply blacklist
        # then create symlinks
        # then return
        if roles is not None:
            roles = self._roles_apply_blacklist_(roles)
            self._create_roles_symlinks_(roles)
            return

        # fallback: create symlink in molecule ephemeral directory
        # to roles directory in project dir which will include all roles
        self._create_symlink_('roles')

    def _create_roles_symlinks_(self, roles):
        (self.get_molecule_ephemeral_directory() / 'roles').mkdir(
            exist_ok=True)
        for role in roles:
            self._create_symlink_('roles/' + role)

    def _create_symlink_(self, path):
        '''Create symlink from molecule ephemeral dir to project dir.'''
        project_dir = self.get_project_dir()
        if project_dir is None:
            return
        source = project_dir / path
        target = self.get_molecule_ephemeral_directory() / path
        try:
            target.symlink_to(source)
        except FileExistsError:
            pass

    def _get_testvars_roles_blacklist_(self):
        return self._testvars_roles_blacklist

    def _get_testvars_roles_whitelist_(self):
        return self._testvars_roles_whitelist

    def _read_playbook_file_from_molecule_yml_(self):
        molecule_yml_path = self.get_molecule_scenario_directory() / \
                            'molecule.yml'
        yaml = YAML(typ='safe')
        try:
            molecule_yml = yaml.load(molecule_yml_path)
            playbook_file = \
                molecule_yml['provisioner']['playbooks']['converge']
            return playbook_file
        except (FileNotFoundError, ScannerError, KeyError):
            return None

    def _read_roles_from_playbook_(self, playbook_file):
        playbook_path = self.get_molecule_scenario_directory() / playbook_file
        yaml = YAML(typ='safe')
        try:
            playbook = yaml.load(playbook_path)
            roles = playbook[0]['roles']
            return roles
        except (FileNotFoundError, ScannerError, KeyError):
            return None

    def _roles_apply_blacklist_(self, roles):
        roles_not_blacklisted = list()
        for role in roles:
            if role not in self._get_testvars_roles_blacklist_():
                roles_not_blacklisted.append(role)
        return roles_not_blacklisted
