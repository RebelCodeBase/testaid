import pytest
import testaid
from testaid.exceptions import TemplatesResolveError


def test_testaid_unit_templates_is_not_none(templates):
    assert templates is not None


def test_testaid_unit_templates_add(templates):
    templates.reset()
    templates.add('{{ my_var}}')
    assert templates._templates == [{'unresolved': '{{ my_var}}'}]


def test_testaid_unit_templates_get_template(templates):
    templates.reset()
    templates.add('{{ my_var}}')
    assert templates.get_template(0) == {'unresolved': '{{ my_var}}'}


def test_testaid_unit_templates_get_templates(templates):
    templates.reset()
    templates.add('{{ my_var}}')
    assert templates.get_templates() == [{'unresolved': '{{ my_var}}'}]


def test_testaid_unit_templates_reset_templates(templates):
    templates._templates = [{'unresolved': '{{ my_var}}'}]
    templates.reset()
    assert templates._templates == []


def test_testaid_unit_templates_resolve_templates(templates,
                                                  monkeypatch):
    playbook_results = [{'ansible_facts': {}},
                        {'msg': '"True"'},
                        {'msg': '""my_value""'}]
    templates_resolved = [{'resolved': '""my_value""',
                           'string': True,
                           'unresolved': '{{ my_var}}'}]
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'run',
                        lambda x: playbook_results)
    templates.reset()
    templates.add('{{ my_var}}')
    templates.resolve()
    assert templates._templates == templates_resolved


def test_testaid_unit_templates_resolve_no_string(templates,
                                                  monkeypatch):
    playbook_results = [{'ansible_facts': {}},
                        {'msg': '"False"'},
                        {'msg': '"99"'}]
    templates_resolved = [{'resolved': '"99"',
                           'string': False,
                           'unresolved': '{{ my_var}}'}]
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'run',
                        lambda x: playbook_results)
    templates.reset()
    templates.add('{{ my_var}}')
    templates.resolve()
    assert templates._templates == templates_resolved


def test_testaid_unit_templates_exception_templatesresolvefailed(
        templates,
        monkeypatch):
    playbook_results = []
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'run',
                        lambda x: playbook_results)
    templates.reset()
    with pytest.raises(TemplatesResolveError) as excinfo:
        templates.resolve()
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Unable to resolve jinja2 templates.'


def test_testaid_unit_templates_add_debug_tasks(templates):
    task_0 = \
        {'action': {'module': 'debug',
                    'args': {'msg': '"{% if {{ my_var }} | string == '
                                    '{{ my_var }} %}True{% '
                                    'else %}False{% endif %}"'}}}
    task_1 = \
        {'action': {'module': 'debug',
                    'args': {'msg': '"{{{{ my_var }} | to_json }}"'}}}
    templates.reset()
    templates._moleculebook.create()
    templates.add('{{ my_var }}')
    templates._add_debug_tasks()
    tasks = templates._moleculebook.get()['tasks']
    assert tasks[0] == task_0
    assert tasks[1] == task_1
