import json
import re


class JsonVars(object):

    def __init__(self,
                 templates,
                 gather_molecule):

        # jinja2 templates
        self._templates = templates

        # unresolved json variables
        self._jsonvars = dict()

        # should we ignore templates containing MOLECULE_ or molecule_file?
        if gather_molecule:
            r = r'(["])?{{(.*?)}}(["])?'
        else:
            r = r'(["])?{{((?:(?!.(?:MOLECULE_|molecule_file)).)*?)}}(["])?'

        # compile regular expression to find templates
        self._regex_templates = re.compile(r)

        # trivial hash table with templates as hash values
        self._hash_table = list()

        # cache table
        self._templates_lookup_table = list()

        self._spots = list()

    def get(self):
        return self._jsonvars

    def get_debug(self):
        msg = '\n'
        msg += self._debug_hash_table_()
        msg += '\n'
        msg += self._debug_templates_lookup_table_()
        msg += '\n'
        msg += self._debug_templates_()
        msg += '\n'
        msg += self._debug_spots_()
        msg += '\n'
        msg += self._debug_jsonvars_()
        msg += '\n'
        return msg

    def reset(self):
        self._templates.reset()
        self._jsonvars = dict()
        self._hash_table = list()
        self._templates_lookup_table = list()
        self._spots = list()

    def resolve(self):

        # first part of query / replace
        self._query_templates_()

        # run a large playbook against the molecule host
        # to resolve all jinja2 templates in one run
        self._templates.resolve()

        # second part of query / replace
        self._replace_templates_()

    def set(self, jsonvars):
        self._jsonvars = jsonvars

    def _query_templates_(self):
        '''Return all unresolved jinja2 templates.'''

        # find all templates in json variables string
        templates_unresolved = \
            self._regex_templates.findall(self._jsonvars)

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

        self._jsonvars = \
            self._regex_templates.sub(lambda x: self._resolve_template_(),
                                      self._jsonvars)

    def _resolve_template_(self):
        '''Replace jinja2 template by resolved template.'''
        spot = self._spots[self._resolve_var_index_]
        index = self._templates_lookup_table[self._resolve_var_index_]
        template = self._templates.get_template(index)

        template_resolved = template['resolved'].strip('"')
        if (template['string'] and spot['left_quote']) \
                or (spot['left_quote'] and not spot['right_quote']):
            template_resolved = '"' + template_resolved
        if (template['string'] and spot['right_quote']) \
                or (spot['right_quote'] and not spot['left_quote']):
            template_resolved = template_resolved + '"'
        self._resolve_var_index_ += 1

        return template_resolved

    def _debug_hash_table_(self):
        msg = '+++ hash_table +++\n'
        for index, hash in enumerate(self._hash_table):
            msg += 'hash ' + str(index) + ' -> ' + str(hash) + '\n'
        return msg

    def _debug_templates_lookup_table_(self):
        msg = '+++ lookup_table +++\n'
        for index, lookup in enumerate(self._templates_lookup_table):
            msg += str(index) + ' -> ' + str(lookup) + '\n'
        return msg

    def _debug_templates_(self):
        msg = '+++ templates +++'
        for index, template in enumerate(self._templates.get_templates()):
            msg += '\ntemplate #' + str(index) + '\n'
            msg += json.dumps(template, indent=4)
        msg += '\n'
        return msg

    def _debug_spots_(self):
        msg = '+++ spots +++'
        for index, spot in enumerate(self._spots):
            msg += '\nspot #' + str(index) + '\n'
            msg += json.dumps(spot, indent=4)
        msg += '\n'
        return msg

    def _debug_jsonvars_(self):
        msg = '+++ jsonvars +++\n'
        msg += str(self._jsonvars)
        msg += '\n'
        return msg
