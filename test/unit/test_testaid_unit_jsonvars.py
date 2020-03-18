import re
import testaid
from testaid.jsonvars import JsonVars


def test_testaid_unit_jsonvars_is_not_none(jsonvars):
    assert jsonvars is not None


def test_testaid_unit_jsonvars_no_localtemplates(
        templates,
        gather_molecule):
    jsonvars = JsonVars(templates,
                        gather_molecule)
    assert jsonvars is not None


def test_testaid_unit_jsonvars_no_gather_molecule(
        templates):
    gather_molecule = False
    jsonvars = JsonVars(templates,
                        gather_molecule)

    r = r'(["])?{{((?:(?!.(?:MOLECULE_|molecule_file)).)*?)}}(["])?'
    regex_templates = re.compile(r)
    assert jsonvars._regex_templates == regex_templates


def test_testaid_unit_jsonvars_get(jsonvars):
    my_jsonvars = '{"my_var": "my_value"}'
    jsonvars._jsonvars = my_jsonvars
    assert jsonvars.get() == my_jsonvars


def test_testaid_unit_jsonvars_resolve(
        jsonvars,
        monkeypatch):
    jsonvars.reset()
    my_template = {'unresolved': 'my_var',
                   'resolved': 'my_value',
                   'string': True}
    monkeypatch.setattr(testaid.templates.Templates,
                        'resolve',
                        lambda x: None)
    monkeypatch.setattr(testaid.templates.Templates,
                        'get_template',
                        lambda x, y: my_template)
    my_jsonvars_unresolved = '{"my_var": "my_value", ' \
                             '"my_template": "{{ my_var }}"}'
    my_jsonvars_resolved = '{"my_var": "my_value", ' \
                           '"my_template": "my_value"}'
    jsonvars._jsonvars = my_jsonvars_unresolved
    jsonvars.resolve()
    assert jsonvars._jsonvars == my_jsonvars_resolved


def test_testaid_unit_jsonvars_resolve_left_quote(
        jsonvars,
        monkeypatch):
    jsonvars.reset()
    my_template = {'unresolved': 'my_var',
                   'resolved': 'my_value',
                   'string': True}
    monkeypatch.setattr(testaid.templates.Templates,
                        'resolve',
                        lambda x: None)
    monkeypatch.setattr(testaid.templates.Templates,
                        'get_template',
                        lambda x, y: my_template)
    my_jsonvars_unresolved = '{"my_var": "my_value", ' \
                             '"my_template": "{{ my_var }}+inline"}'
    my_jsonvars_resolved = '{"my_var": "my_value", ' \
                           '"my_template": "my_value+inline"}'
    jsonvars._jsonvars = my_jsonvars_unresolved
    jsonvars.resolve()
    assert jsonvars._jsonvars == my_jsonvars_resolved


def test_testaid_unit_jsonvars_resolve_right_quote(
        jsonvars,
        monkeypatch):
    jsonvars.reset()
    my_template = {'unresolved': 'my_var',
                   'resolved': 'my_value',
                   'string': True}
    monkeypatch.setattr(testaid.templates.Templates,
                        'resolve',
                        lambda x: None)
    monkeypatch.setattr(testaid.templates.Templates,
                        'get_template',
                        lambda x, y: my_template)
    my_jsonvars_unresolved = '{"my_var": "my_value", ' \
                             '"my_template": "inline+{{ my_var }}"}'
    my_jsonvars_resolved = '{"my_var": "my_value", ' \
                           '"my_template": "inline+my_value"}'
    jsonvars._jsonvars = my_jsonvars_unresolved
    jsonvars.resolve()
    assert jsonvars._jsonvars == my_jsonvars_resolved


def test_testaid_unit_jsonvars_resolve_cache(
        jsonvars,
        monkeypatch):
    jsonvars.reset()
    my_template = {'unresolved': 'my_var',
                   'resolved': 'my_value',
                   'string': True}
    monkeypatch.setattr(testaid.templates.Templates,
                        'resolve',
                        lambda x: None)
    monkeypatch.setattr(testaid.templates.Templates,
                        'get_template',
                        lambda x, y: my_template)
    my_jsonvars_unresolved = '{"my_var": "my_value", ' \
                             '"my_template1": "{{ my_var }}",' \
                             '"my_template2": "{{ my_var }}"}'
    my_jsonvars_resolved = '{"my_var": "my_value", ' \
                           '"my_template1": "my_value",' \
                           '"my_template2": "my_value"}'
    jsonvars._jsonvars = my_jsonvars_unresolved
    jsonvars.resolve()
    assert jsonvars._jsonvars == my_jsonvars_resolved


def test_testaid_unit_jsonvars_set(jsonvars):
    my_jsonvars = '{"my_var": "my_value"}'
    jsonvars.set(my_jsonvars)
    assert jsonvars._jsonvars == my_jsonvars


def test_testaid_unit_jsonvars_debug(jsonvars,
                                     monkeypatch):
    jsonvars.reset()
    my_template = {'unresolved': 'my_var',
                   'resolved': 'my_value',
                   'string': True}
    monkeypatch.setattr(testaid.templates.Templates,
                        'resolve',
                        lambda x: None)
    monkeypatch.setattr(testaid.templates.Templates,
                        'get_template',
                        lambda x, y: my_template)
    my_jsonvars_unresolved = '{"my_var": "my_value", ' \
                             '"my_template1": "{{ my_var }}",' \
                             '"my_template2": "{{ my_var }}"}'
    my_jsonvars_debug = '''\

+++ hash_table +++
hash 0 ->  my_var 
hash 1 ->  my_var 

+++ lookup_table +++
0 -> 0
1 -> 0

+++ templates +++
template #0
{
    "unresolved": "my_var"
}

+++ spots +++
spot #0
{
    "left_quote": true,
    "right_quote": true
}
spot #1
{
    "left_quote": true,
    "right_quote": true
}

+++ jsonvars +++
{"my_var": "my_value", "my_template1": "my_value","my_template2": "my_value"}

'''  # noqa W291
    jsonvars._jsonvars = my_jsonvars_unresolved
    jsonvars.resolve()
    jsonvars_debug = jsonvars.get_debug()
    assert jsonvars_debug == my_jsonvars_debug
