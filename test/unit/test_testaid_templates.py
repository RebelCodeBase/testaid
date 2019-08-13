def test_testaid_templates_is_not_none(templates):
    assert templates is not None


def test_testaid_templates_add(templates):
    templates.reset()
    templates.add('{{ my_var}}')
    assert templates._templates == [{'unresolved': '{{ my_var}}'}]


def test_testaid_templates_get_template(templates):
    templates.reset()
    templates.add('{{ my_var}}')
    assert templates.get_template(0) == {'unresolved': '{{ my_var}}'}


def test_testaid_templates_get_templates(templates):
    templates.reset()
    templates.add('{{ my_var}}')
    assert templates.get_templates() == [{'unresolved': '{{ my_var}}'}]


def test_testaid_templates_reset_templates(templates):
    templates._templates = [{'unresolved': '{{ my_var}}'}]
    templates.reset()
    assert templates._templates == []


def test_testaid_templates_add_debug_tasks(templates):
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
