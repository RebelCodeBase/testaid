import json


class JsonVarsDebug(object):

    def debug_hash_table(self, hashtable):
        msg = '+++ hash_table +++\n'
        for index, hash in enumerate(hashtable):
            msg += 'hash ' + str(index) + ' -> ' + str(hash) + '\n'
        return msg

    def debug_templates_lookup_table(self, lookup_table):
        msg = '+++ lookup_table +++\n'
        for index, lookup in enumerate(lookup_table):
            msg += str(index) + ' -> ' + str(lookup) + '\n'
        return msg

    def debug_templates(self, templates):
        msg = '+++ templates +++'
        for index, template in enumerate(templates):
            msg += '\ntemplate #' + str(index) + '\n'
            msg += json.dumps(template, indent=4)
        msg += '\n'
        return msg

    def debug_spots(self, spots):
        msg = '+++ spots +++'
        for index, spot in enumerate(spots):
            msg += '\nspot #' + str(index) + '\n'
            msg += json.dumps(spot, indent=4)
        msg += '\n'
        return msg

    def debug_jsonvars(self, jsonvars):
        msg = '+++ jsonvars +++\n'
        msg += jsonvars
        msg += '\n'
        return msg

    def get(self, jsonvars):
        msg = ''
        msg += self.debug_hash_table(jsonvars._hash_table)
        msg += '\n'
        msg += self.debug_templates_lookup_table(
            jsonvars._templates_lookup_table)
        msg += '\n'
        msg += self.debug_templates(jsonvars._templates.get_templates())
        msg += '\n'
        msg += self.debug_spots(jsonvars._spots)
        msg += '\n'
        msg += self.debug_jsonvars(jsonvars._jsonvars)
        return msg
