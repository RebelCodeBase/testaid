import json
from testaid.jsonvars import JsonVars
from testaid.templates import Templates


class TestVars(object):
    '''Expose ansible variabless of a molecule scenario.

    Include ansible facts form molecule host.
    Include roles from ansible project directory.
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

        # jinja2 templates class
        templates = Templates(self._moleculebook)

        # this variable will be returned by the testvars fixture
        self._testvars = dict()

        # get ansible variables
        testvars_unresolved = self._moleculebook.get_vars(resolve_vars,
                                                          gather_facts,
                                                          extra_vars)

        if not resolve_vars:

            # save vars offline gathered
            self._testvars = testvars_unresolved

        else:

            # convert python variables to json
            self._testvars_unresolved_json = json.dumps(testvars_unresolved)

            # create JsonVars instance with unresolved json variables
            self._jsonvars = JsonVars(templates,
                                      self._testvars_unresolved_json,
                                      gather_molecule)

            # get resolved json variables
            self._testvars_resolved_json = self._jsonvars.get_resolved()

            # convert json variables to python
            self._testvars = json.loads(self._testvars_resolved_json)

    def get_testvars(self):
        return self._testvars
