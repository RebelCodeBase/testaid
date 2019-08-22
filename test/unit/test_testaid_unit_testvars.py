import pytest
import re
import testaid
from testaid.testvars import TestVars
from testaid.exceptions import AnsibleRunError


def test_testaid_unit_testvars_is_not_none(
        moleculebook,
        jsonvars,
        resolve_vars,
        gather_facts,
        extra_vars):
    gatherfrom_moleculehost = True
    with pytest.raises(AnsibleRunError):
        TestVars(moleculebook,
                 jsonvars,
                 resolve_vars,
                 gatherfrom_moleculehost,
                 gather_facts,
                 extra_vars).get_testvars()


def test_testaid_unit_testvars_no_resolve_vars(
        moleculebook,
        jsonvars):
    resolve_vars = False
    gatherfrom_moleculehost = False
    gather_facts = False
    extra_vars = ''
    testvars = TestVars(moleculebook,
                        jsonvars,
                        resolve_vars,
                        gatherfrom_moleculehost,
                        gather_facts,
                        extra_vars).get_testvars()
    assert 'inventory_hostname' in testvars


def test_testaid_unit_testvars_resolve_vars(
        moleculebook,
        jsonvars,
        monkeypatch):

    testvars_unresolved = \
        {'my_var_1': 'my_value', 'my_var_2': '{{ my_var_1 }}'}
    jsonvars_resolved = \
        '{"my_var_1": "my_value", "my_var_2": "my_value"}'
    testvars_resolved = \
        {'my_var_1': 'my_value', 'my_var_2': 'my_value'}
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook,
                        'get_vars',
                        lambda w, x, y, z: testvars_unresolved)
    monkeypatch.setattr(testaid.jsonvars.JsonVars,
                        'resolve',
                        lambda x: None)
    monkeypatch.setattr(testaid.jsonvars.JsonVars,
                        'get',
                        lambda x: jsonvars_resolved)
    resolve_vars = True
    gatherfrom_moleculehost = False
    gather_facts = False
    extra_vars = ''
    testvars = TestVars(moleculebook,
                        jsonvars,
                        resolve_vars,
                        gatherfrom_moleculehost,
                        gather_facts,
                        extra_vars).get_testvars()
    assert testvars == testvars_resolved


def test_testaid_unit_testvars_cache_key(cache_key):
    assert re.match('testvars/+', cache_key)


def test_testaid_unit_testvars_gatherfrom_moleculehost(
        gatherfrom_moleculehost):
    assert gatherfrom_moleculehost
