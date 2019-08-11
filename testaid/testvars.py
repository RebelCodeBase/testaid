import json
import re
from testaid.templates import Templates

class TestVars(object):
    '''Expose ansible variabless of a molecule scenario.

    Use by pytest fixture for testinfra.
    Include ansible facts form molecule host.
    Include roles from project directory.
    Resolve jinja2 template variables.
    '''

    def __init__(self,
                 moleculebook,
                 resolve_vars,
                 gather_facts,
                 gather_molecule,
                 extra_vars):

        # use moleculebook fixture to resolve templates
        self._moleculebook = moleculebook

        # this variable will be returned by the testvars fixture
        self._testvars = dict()

        # jinja2 templates
        self._templates = Templates(self._moleculebook)

        # get ansible variables
        testvars_unresolved = self._moleculebook.get_vars(resolve_vars,
                                                          gather_facts,
                                                          extra_vars)

        if not resolve_vars:

            # save offline gathered vars
            self._testvars = testvars_unresolved

        else:

            # should we ignore templates containing MOLECULE_ or molecule_file?
            if gather_molecule:
                r = r'(["])?{{(.*?)}}(["])?'
            else:
                r = r'(["])?{{((?:(?!.(?:MOLECULE_|molecule_file)).)*?)}}(["])?'  # noqa E501

            # compile regular expression to find templates
            self._regex_templates = re.compile(r)

            # convert unresolved test vars to json
            self._testvars_unresolved_json = json.dumps(testvars_unresolved)

            # first part of query / replace
            self._query_templates_()

            # run a large playbook against the molecule host
            # to resolve all jinja2 templates in one run
            self._templates.resolve()

            # second part of query / replace
            self._replace_templates_()

    def get_testvars(self):
        return self._testvars

    def _query_templates_(self):
        '''Return all unresolved jinja2 templates.'''

        # trivial hash table with templates as hash values
        self._hash_table = list()

        # cache table
        self._templates_lookup_table = list()

        # how do the templates look like?
        #self._templates = list()

        # where have the templates been found?
        self._spots = list()

        # find all templates in json variables string
        templates_unresolved = \
            self._regex_templates.findall(self._testvars_unresolved_json)

        # create hash table so that we don't resolve templates twice
        for template_unresolved in templates_unresolved:
            self._hash_table.append(template_unresolved[1])

        for index, template_unresolved in enumerate(templates_unresolved):
            spot = dict()

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

            # get first occurence of our template
            first = self._hash_table.index(template_unresolved[1])

            # check if this is a double template
            if first < index:

                # existing template
                reference = self._templates_lookup_table[first]
                self._templates_lookup_table.append(reference)

            else:

                # new template
                self._templates_lookup_table.append(
                    len(self._templates.get_templates()))
                self._templates.add(template_unresolved[1].strip())

    def _replace_templates_(self):
        '''Replace jinja2 templates by resolved templates.'''

        # keep track of the position in self._templates_resolved
        self._resolve_var_index_ = 0

        self._testvars_unresolved_json = \
            self._regex_templates.sub(lambda x: self._resolve_template_(),
                                      self._testvars_unresolved_json)

        # print debug data
        # self._debug_print_()

        self._testvars = json.loads(self._testvars_unresolved_json)

    def _resolve_template_(self):
        '''Replace jinja2 template by resolved template.'''
        spot = self._spots[self._resolve_var_index_]
        index = self._templates_lookup_table[self._resolve_var_index_]
        template = self._templates.get(index)

        template_resolved = template['resolved'].strip('"')
        if (template['string'] and spot['left_quote']) \
                or (spot['left_quote'] and not spot['right_quote']):
            template_resolved = '"' + template_resolved
        if (template['string'] and spot['right_quote']) \
                or (spot['right_quote'] and not spot['left_quote']):
            template_resolved = template_resolved + '"'
        self._resolve_var_index_ += 1

        return template_resolved

    def _debug_print_(self):
        self._debug_print_hash_table_()
        self._debug_print_templates_lookup_table_()
        self._debug_print_templates_()
        self._debug_print_spots_()
        self._debug_print_playbook_()
        self._debug_print_testvars_unresolved_json_()
        self._debug_print_testvars_()

    def _debug_print_hash_table_(self):
        print("\n\nhash_table\n")
        for index, hash in enumerate(self._hash_table):
            print('hash ' + str(index) + ' -> ' + str(hash))

    def _debug_print_templates_lookup_table_(self):
        print("\n\nlookup_table\n")
        for index, lookup in enumerate(self._templates_lookup_table):
            print(str(index) + ' -> ' + str(lookup))

    def _debug_print_templates_(self):
        print("\n\ntemplates\n")
        for index, template in enumerate(self._templates.get_templates()):
            print('template #' + str(index))
            print(json.dumps(template, indent=4))

    def _debug_print_spots_(self):
        print("\n\nspots\n")
        for index, spot in enumerate(self._spots):
            print('spot #' + str(index))
            print(json.dumps(spot, indent=4))

    def _debug_print_playbook_(self):
        print("\n\nplaybook\n")
        print(json.dumps(self._moleculebook.get(), indent=4))

    def _debug_print_testvars_unresolved_json_(self):
        print("\n\ntestvars_unresolved_json\n")
        print(self._testvars_unresolved_json)

    def _debug_print_testvars_(self):
        print("\n\ntestvars\n")
        print(json.dumps(self._testvars, indent=4))
