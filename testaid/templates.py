from math import floor
from testaid.exceptions import TemplatesResolveError


class Templates(object):

    def __init__(self, moleculebook):
        self._moleculebook = moleculebook
        self._templates = list()

    def add(self, jinja2):
        template = dict()
        template['unresolved'] = jinja2
        self._templates.append(template)

    def get_template(self, index):
        return self._templates[index]

    def get_templates(self):
        return self._templates

    def reset(self):
        self._templates = list()

    def resolve(self):
        '''Resolve all variables of a play managed by molecule.'''

        # reset playbook to default
        self._moleculebook.create()

        # populate playbook with task
        self._add_debug_tasks()

        # run playbook to resolve vars
        playbook_results = self._moleculebook.run()

        # scrutinize playbook results
        self._gather_results(playbook_results)

    def _gather_results(self, playbook_results):
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
                    self._templates[template_index]['resolved'] = \
                        template_resolved
        except (IndexError, KeyError):
            raise TemplatesResolveError('Unable to resolve jinja2 templates.')

    def _add_debug_tasks(self):
        for template in self._templates:
            unres = template['unresolved']

            # add debug task to test if the template is a string
            self._moleculebook.add_task_debug(
                '"{% if ' + unres + ' | string == ' + unres + ' %}' +
                'True{% else %}False{% endif %}"')

            # add a debug task to resolve jinja2 template
            self._moleculebook.add_task_debug('"{{' + unres + ' | to_json }}"')
