import json


class JsonVarsDebug(object):

    def debug_hash_table(self, hashtable):
        msg = "\n\nhash_table\n"
        for index, hash in enumerate(hashtable):
            msg += 'hash ' + str(index) + ' -> ' + str(hash)
        return msg

    def debug_templates_lookup_table(self, lookup_table):
        msg = "\n\nlookup_table\n"
        for index, lookup in enumerate(lookup_table):
            msg += str(index) + ' -> ' + str(lookup)
        return msg

    def debug_templates(self, templates):
        msg = "\n\ntemplates\n"
        for index, template in enumerate(templates):
            msg += 'template #' + str(index)
            msg += json.dumps(template, indent=4)
        return msg

    def debug_spots(self, spots):
        msg = "\n\nspots\n"
        for index, spot in enumerate(spots):
            msg += 'spot #' + str(index)
            msg += json.dumps(spot, indent=4)
        return msg

    def debug_jsonvars_unresolved(self, jsonvars):
        msg = "\n\njsonvars_unresolved\n"
        msg += jsonvars
        return msg

    def get(self):
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
