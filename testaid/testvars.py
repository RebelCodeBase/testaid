import json
import os
import pytest
import re

@pytest.fixture(scope='module')
def testvars(request, host):
    try:
        cache_id = 'testvars' + os.environ['MOLECULE_EPHEMERAL_DIRECTORY']
    except:
        cache_id = 'testvars/global'
    testvars = request.config.cache.get(cache_id, None)
    if testvars is None:
        testvars = Testvars(host).testvars
        request.config.cache.set(cache_id, testvars)
    return testvars


class Testvars(object):

    def __init__(self, host):
        self.host = host
        self.testvars = {}

        # try to use ephemeral molecule directory to store unresolved testvars
        try:
            tempdir = os.environ['MOLECULE_EPHEMERAL_DIRECTORY']
        except:
            tempdir = '/tmp'

        # create json file for unresolved testvars
        self.testvars_dumpfilename = tempdir + '/testvars_unresolved.json'
        testvars_dumpfile = open(self.testvars_dumpfilename, 'w')

        # get variables from defaults/main.yml files of all roles
        testvars_unresolved = self._include_roles_defaults_()

        # respect variable precedence by updating variables with
        # global ansible variables provided by testinfra ansible module
        testvars_unresolved.update(self.host.ansible.get_variables())

        # convert unresolved test vars to json in order
        # to replace the templated variables through a regular exrpression
        self.testvars_unresolved_json = json.dumps(testvars_unresolved)

        # store unresolved testvars as json in a file as input to
        # the ansible debug module via command line --extra-vars
        testvars_dumpfile.write(self.testvars_unresolved_json)
        testvars_dumpfile.close()

        # resolve jinja2 templates by leveraging the ansible debug
        # module through the testinfra ansible module
        self._resolve_vars_()

    def _get_roles_dir_(self):

        # use the molecule scenario directory as a starting point
        try:
            path = os.environ['MOLECULE_SCENARIO_DIRECTORY']
        except:
            return None

        # move up until we find a roles directory
        while path != '/':
            path = os.path.dirname(path)
            if 'roles' in os.listdir(path):
                return path + '/roles'

        return None

    def _include_roles_defaults_(self):
        # filenames of the default/main.yml files
        roles_defaults = {}

        # get roles dir starting at the molecule scenario directory
        roles_dir = self._get_roles_dir_()

        if roles_dir:
            # get roles as subdirectories of the role directory
            roles = next(os.walk(roles_dir))[1]

            for role in roles:
                file_role_defaults = roles_dir + '/' + role + "/defaults/main.yml"
                if os.path.isfile(file_role_defaults):

                    # use ansible include_vars module to read role defaults
                    role_defaults = \
                        self.host.ansible("include_vars",
                                          "file="
                                          + file_role_defaults)['ansible_facts']

                    # the defaults of each role should be prefixed with the
                    # role name to avoid collisions
                    roles_defaults.update(role_defaults)

        return roles_defaults

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
        kwargs = {'extravars': '--extra-vars=@' + self.testvars_dumpfilename}

        # use ansible debug module to resolve template
        template_resolved = str(self.host.ansible('debug', 'msg=' + template_unresolved, **kwargs)['msg'])

        # escape resolved template
        template_resolved = json.dumps(template_resolved).strip('"')

        return template_resolved
