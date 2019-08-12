import json


class TestVars(object):
    '''Expose ansible variabless of a molecule scenario.

    Include ansible facts form molecule host.
    Include roles from ansible project directory.
    Resolve jinja2 template variables.
    '''

    def __init__(self,
                 moleculebook,
                 jsonvars,
                 resolve_vars,
                 gather_facts,
                 extra_vars):

        # this variable will be returned by the testvars fixture
        self._testvars = dict()

        # get ansible variables
        testvars_unresolved = moleculebook.get_vars(resolve_vars,
                                                    gather_facts,
                                                    extra_vars)

        if not resolve_vars:

            # save vars offline gathered
            self._testvars = testvars_unresolved

        else:

            # convert python variables to json
            testvars_unresolved_json = json.dumps(testvars_unresolved)

            # set jsonvars to unresolved testvars
            jsonvars.set(testvars_unresolved_json)

            # resolve unresolved json testvars
            jsonvars.resolve()

            # get resolved testvars from jsonvars
            testvars_resolved_json = jsonvars.get()

            # convert json vars to python
            self._testvars = json.loads(testvars_resolved_json)

    def get_testvars(self):
        return self._testvars
