import json
from math import floor
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
        self._templates = list()
        self._templates_lookup_table = list()

        # get ansible variables
        testvars_unresolved = self._moleculebook.get_vars()

        # convert unresolved test vars to json
        self._testvars_unresolved_json = json.dumps(testvars_unresolved)

        # regular expression to find templates
        self._regex_templates = r'(["])?{{(.*?)}}(["])?'

        # first part of query / replace
        self._query_templates_()

        # run a large playbook against the molecule host
        # to resolve all jinja2 templates in one run
        self._resolve_templates_()

        # second part of query / replace
        self._replace_templates_()

    def get_testvars(self):
        return self._testvars

    def _query_templates_(self):
        '''Return all unresolved jinja2 templates.'''

        # find all templates in json variables string
        templates_unresolved = re.findall(self._regex_templates,
                                          self._testvars_unresolved_json)

        for index, template_unresolved in enumerate(templates_unresolved):
            template = dict()

            # fill a lookup table so that we don't resolve templates twice
            first = templates_unresolved.index(template_unresolved)
            if first < index:

                # existing entry
                self._templates_lookup_table.append(first)
            else:

                # new entry
                self._templates_lookup_table.append(index)

                template['unresolved'] = template_unresolved[1].strip()
                if template_unresolved[0]:
                    template['left_quote'] = True
                else:
                    template['left_quote'] = False
                if template_unresolved[2]:
                    template['right_quote'] = True
                else:
                    template['right_quote'] = False
                self._templates.append(template)

    def _resolve_templates_(self):
        '''Resolve all variables of a play managed by molecule.'''
        templates_resolved = list()

        # reset playbook
        self._moleculebook.create()

        # add one debug task for each unresolved template
        for index, dest in enumerate(self._templates_lookup_table):
            if index == dest:
                unres = self._templates[index]['unresolved']
                self._moleculebook.add_task_debug(
                    '"{% if ' + unres + ' | string == ' + unres + ' %}' +
                    'True{% else %}False{% endif %}"')
                self._moleculebook.add_task_debug('"{{' + unres + ' | to_json }}"')

        playbook_results = self._moleculebook.run()

        try:

            # delete ansible_facts task result
            del playbook_results[0]

            for index, playbook_result in enumerate(playbook_results):
                template_index = floor(index/2)
                if (index % 2) == 0:
                    if playbook_result['msg'].strip('"') == 'True':
                        self._templates[template_index]['string'] = True
                    else:
                        self._templates[template_index]['string'] = False
                else:
                    template_resolved = playbook_result['msg']
                    self._templates[template_index]['resolved'] = template_resolved
        except:

            # TODO: do not catch all
            # TODO: raise exception
            print('\n+++++++++++++++++++++++++++++++++++++++'
            '+++++++++++++++++++++++++++++++++++++++++')
            print('[TestVars::_resolve_templates_] '
            'Unable to resolve jinja2 templates.')
            print('+++++++++++++++++++++++++++++++++++++++++'
            '+++++++++++++++++++++++++++++++++++++++\n')

    def _replace_templates_(self):
        '''Replace jinja2 templates by resolved templates.'''
        # keep track of the position in self._templates_resolved
        self._resolve_var_index_ = 0

        testvars_json = \
            re.sub(self._regex_templates,
                   lambda x: self._resolve_template_(),
                   self._testvars_unresolved_json)

        self._testvars = json.loads(testvars_json)

    def _resolve_template_(self):
        '''Replace jinja2 template by resolved template.'''

        index = self._templates_lookup_table[self._resolve_var_index_]
        template = self._templates[index]

        template_resolved = template['resolved'].strip('"')
        if template['string'] and template['left_quote']:
            template_resolved = '"' + template_resolved
        if template['string'] and template['right_quote']:
            template_resolved = template_resolved + '"'
        self._resolve_var_index_ += 1

        return template_resolved
