import re
from testaid.jsonvarsdebug import JsonVarsDebug


class JsonVars(object):

    def __init__(self,
                 templates,
                 jsonvars_unresolved,
                 gather_molecule):

        # instance of Templates class with moleculebook
        self._templates = templates

        # unresolved json variables
        self._jsonvars_unresolved = jsonvars_unresolved

        # resolved json variables (after calling self.resolve()
        self._jsonvars_resolved = jsonvars_unresolved

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

        # where have the templates been found?
        self._spots = list()

    def debug(self):
        jsonvarsdebug = JsonVarsDebug()
        msg = ''
        msg += jsonvarsdebug.debug_hash_table(
            self._hash_table)
        msg += jsonvarsdebug.debug_templates_lookup_table(
            self._templates_lookup_table)
        msg += jsonvarsdebug.debug_templates(
            self._templates.get_templates())
        msg += jsonvarsdebug.debug_spots(
            self._spots)
        msg += jsonvarsdebug.debug_jsonvars_unresolved(
            self._jsonvars_unresolved)
        return msg

    def get_resolved(self):
        return self._jsonvars_resolved

    def resolve(self):

        # first part of query / replace
        self._query_templates_()

        # run a large playbook against the molecule host
        # to resolve all jinja2 templates in one run
        self._templates.resolve()

        # second part of query / replace
        self._replace_templates_()

    def _query_templates_(self):
        '''Return all unresolved jinja2 templates.'''

        # find all templates in json variables string
        templates_unresolved = \
            self._regex_templates.findall(self._jsonvars_unresolved)

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

        self._jsonvars_resolved = \
            self._regex_templates.sub(lambda x: self._resolve_template_(),
                                      self._jsonvars_unresolved)

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
