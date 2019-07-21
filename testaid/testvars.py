import json
import os
import re
from pathlib import Path

class Testvars(object):

    def __init__(self, host, tmp_path):
        self.host = host
        self.testvars = {}

        # create json file for unresolved testvars
        self.testvars_unresolved_json_file = \
            tmp_path / 'testvars_unresolved.json'

        testvars_unresolved = {}

        # -> ansible_facts
        # get ansible_facts gathered by gather_facts: true
        testvars_unresolved.update(self._add_ansible_facts_())

        # -> roles defaults variables
        # get variables from defaults/main.yml file of all roles
        testvars_unresolved.update(self._include_roles_variables_('defaults'))

        # -> testinfra ansible variables
        # respect variable precedence by updating variables with
        # global ansible variables provided by testinfra ansible module
        testvars_unresolved.update(self.host.ansible.get_variables())

        # -> project vars variables
        # get variables from all files in vars directory of project
        testvars_unresolved.update(self._include_project_vars_('vars'))

        # -> roles vars variables
        # get variables from vars/main.yml file of all roles
        testvars_unresolved.update(self._include_roles_variables_('vars'))

        # -> extra vars variables
        # get variables from TESTAID_EXTRA_VARS_FILES environment variable
        testvars_unresolved.update(self._include_extra_vars_())

        # convert unresolved test vars to json in order
        # to replace the templated variables through a regular exrpression
        self.testvars_unresolved_json = json.dumps(testvars_unresolved)

        # store unresolved testvars as json in a file as input to
        # the ansible debug module via command line --extra-vars
        self.testvars_unresolved_json_file.write_text(self.testvars_unresolved_json)

        # resolve jinja2 templates by leveraging the ansible debug
        # module through the testinfra ansible module
        self._resolve_vars_()

    def _get_project_dir_(self):

        # use the molecule scenario directory as a starting point
        try:
            path = Path(os.environ['MOLECULE_SCENARIO_DIRECTORY'])
        except:
            return None

        # move up until we find a roles directory
        while path != Path('/'):
            path = path.parent
            if path / 'roles' in [d for d in path.iterdir() if d.is_dir()]:
                return path

        return None

    def _add_ansible_facts_(self):
        return self.host.ansible('setup')

    def _include_vars_file_(self, filepath):
        return self.host.ansible(
            'include_vars',
            'file=' + filepath)['ansible_facts']

    def _include_roles_variables_(self, path):
        roles_variables = {}

        project_dir = self._get_project_dir_()

        if project_dir:

            roles_dir = project_dir / 'roles'

            # get roles as subdirectories of the role directory
            roles = [d for d in roles_dir.iterdir() if d.is_dir()]

            for role in roles:

                # build target path
                # ansible only permits main.yml in role defaults and vars
                role_variables_file = role / path / 'main.yml'

                if role_variables_file.is_file():

                    # use ansible include_vars module to read role variables
                    role_defaults = self._include_vars_file_(
                        str(role_variables_file))

                    # the variables of each role should be prefixed with the
                    # role name to avoid collisions
                    roles_variables.update(role_defaults)

        return roles_variables

    def _include_project_vars_(self, path):
        vars = {}

        project_dir = self._get_project_dir_()

        if project_dir:

            vars_dir = project_dir / 'vars'

            # loop over files in vars directory
            for vars_file in vars_dir.rglob('*.yml'):

                # use ansible include_vars module to read vars variables
                vars_file_variables = self._include_vars_file_(
                    str(vars_dir / vars_file))

                vars.update(vars_file_variables)

        return vars

    def _include_extra_vars_(self):
        extra_vars = {}

        if 'MOLECULE_SCENARIO_DIRECTORY' not in os.environ.keys():
            return extra_vars

        molecule_scenario_directory = \
            Path(os.environ['MOLECULE_SCENARIO_DIRECTORY'])

        # only continue if environment variable is set:
        # molecule.yml -> verifier -> env -> TESTAID_EXTRA_VARS_FILES
        if 'TESTAID_EXTRA_VARS_FILES' not in os.environ.keys():
            return extra_vars

        extra_vars_files = []

        # extra vars files must be separated wit a colon
        for file in os.environ['TESTAID_EXTRA_VARS_FILES'].split(':'):
            extra_vars_files.append(molecule_scenario_directory / file)

        for extra_vars_file in extra_vars_files:

            if extra_vars_file.is_file():
    
                # use ansible include_vars module to read extra vars variables
                extra_vars_file_variables = self._include_vars_file_(
                    str(extra_vars_file))

                extra_vars.update(extra_vars_file_variables)

        return extra_vars

    def _resolve_vars_(self):

        # resolve templates
        regex_templates = r'{{.*?}}'
        testvars_json = \
            re.sub(regex_templates,
                   lambda match: self._resolve_template_(match.group(0)),
                   self.testvars_unresolved_json,
                   flags=re.S)

        # load json and unescape characters
        self.testvars = json.loads(testvars_json)

    def _resolve_template_(self, template_unresolved):

        # prepare arguments variable to pass
        # dumped testvars to ansible debug module
        kwargs = {'extravars': '--extra-vars=@' + str(self.testvars_unresolved_json_file)}

        # use ansible debug module to resolve template
        template_resolved = str(self.host.ansible('debug', 'msg=' + template_unresolved, **kwargs)['msg'])

        # escape resolved template
        template_resolved = json.dumps(template_resolved).strip('"')

        return template_resolved
