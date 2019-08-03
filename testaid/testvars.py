import json
import re


class TestVars(object):
    '''Expose ansible variabless of a molecule scenario.

    Use by pytest fixture for testinfra.
    Include ansible facts form molecule host.
    Include roles from project directory.
    Resolve jinja2 template variables.
    '''

    def __init__(self, moleculebook):
        self._moleculebook = moleculebook
        self._testvars = dict()

        # get ansible variables
        testvars_unresolved = self._moleculebook.get_vars()

        # convert unresolved test vars to json
        self._testvars_unresolved_json = json.dumps(testvars_unresolved)

        # regular expression to find templates
        # we are scanning json so
        # two consecutive curly braces
        # could also mean dict of dict :-(
        self._regex_templates = r'{{.*?}}'

        # first part of query / replace
        self._templates_unresolved = self._query_templates_()

        # run a large playbook against the molecule host
        # to resolve all jinja2 templates in one run
        self._templates_resolved = self._resolve_templates_()

        # second part of query / replace
        self._testvars = self._replace_templates_()

    def get_testvars(self):
        return self._testvars

    def _query_templates_(self):
        '''Return all unresolved jinja2 templates.'''
        templates_unresolved = re.findall(self._regex_templates,
                                          self._testvars_unresolved_json)
        return templates_unresolved

    def _resolve_templates_(self):
        '''Resolve all variables of a play managed by molecule.'''
        templates_resolved = list()

        # reset playbook
        self._moleculebook.create()

        # add one debug task for each unresolved template
        for template_unresolved in self._templates_unresolved:
            self._moleculebook.add_task_debug('"' + template_unresolved + '"')

        playbook_results = self._moleculebook.run()

        try:
            # delete ansible_facts task result
            del playbook_results[0]

            for playbook_result in playbook_results:
                templates_resolved.append(playbook_result['msg'].strip('"'))
        except:
            print('\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('[TestVars::_resolve_templates_] Unable to resolve jinja2 templates.')
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')

        return templates_resolved

    def _replace_templates_(self):
        '''Replace jinja2 templates by resolved templates.'''
        # keep track of the position in self._templates_resolved
        self._resolve_var_index_ = 0

        testvars_json = \
            re.sub(self._regex_templates,
                   lambda match: self._resolve_template_(match.group(0)),
                   self._testvars_unresolved_json)

        # load json and unescape characters
        return json.loads(testvars_json)

    def _resolve_template_(self, template_unresolved):
        '''Replace jinja2 template by resolved template.'''
        template_resolved = self._templates_resolved[self._resolve_var_index_]
        self._resolve_var_index_ = self._resolve_var_index_ + 1
        return str(template_resolved)
