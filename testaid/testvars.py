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

        # this is what we are looking for
        self._testvars = dict()

        # what are the themplate?
        self._templates = list()

        # where are the templates?
        self._spots = list()

        # cache templates
        self._templates_lookup_table = list()

        # get ansible variables
        testvars_unresolved = self._moleculebook.get_vars()

        # convert unresolved test vars to json
        self._testvars_unresolved_json = json.dumps(testvars_unresolved)

        # regular expression to find templates
        self._regex_templates = re.compile(r'(["])?{{(.*?)}}(["])?')

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
        hash_table = list()

        # find all templates in json variables string
        templates_unresolved = \
            self._regex_templates.findall(self._testvars_unresolved_json)

        # create a trivial hash table with the templates as hash values
        for template_unresolved in templates_unresolved:
             hash_table.append(template_unresolved[1])

        for index, template_unresolved in enumerate(templates_unresolved):
            spot = dict()
            template = dict()

            # save template spot environment
            if template_unresolved[0]:
                spot['left_quote'] = True
            else:
                spot['left_quote'] = False
            if template_unresolved[2]:
                spot['right_quote'] = True
            else:
                spot['right_quote'] = False
            self._spots.append(spot)

            # populate a lookup table so that we don't resolve templates twice
            first = hash_table.index(template_unresolved[1])

            if first < index:

                # existing entry
                reference = self._templates_lookup_table[first]
                self._templates_lookup_table.append(reference)

            else:

                # new entry
                self._templates_lookup_table.append(len(self._templates))

                # create
                template['unresolved'] = template_unresolved[1].strip()
                self._templates.append(template)

    def _resolve_templates_(self):
        '''Resolve all variables of a play managed by molecule.'''
        templates_resolved = list()

        # reset playbook
        self._moleculebook.create()

        # add one debug task for each unresolved template
        for template in self._templates:
            unres = template['unresolved']
            self._moleculebook.add_task_debug(
                '"{% if ' + unres + ' | string == ' + unres + ' %}' +
                'True{% else %}False{% endif %}"')
            self._moleculebook.add_task_debug('"{{' + unres + ' | to_json }}"')

        # run playbook to resolve vars
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

            # TODO: do not catch all exceptions
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
            self._regex_templates.sub(lambda x: self._resolve_template_(),
                                      self._testvars_unresolved_json)

        self._testvars = json.loads(testvars_json)

    def _resolve_template_(self):
        '''Replace jinja2 template by resolved template.'''
        spot = self._spots[self._resolve_var_index_]
        index = self._templates_lookup_table[self._resolve_var_index_]
        template = self._templates[index]

        template_resolved = template['resolved'].strip('"')
        if template['string'] and spot['left_quote']:
            template_resolved = '"' + template_resolved
        if template['string'] and spot['right_quote']:
            template_resolved = template_resolved + '"'
        self._resolve_var_index_ += 1

        return template_resolved
