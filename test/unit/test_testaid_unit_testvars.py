import pytest
from testaid.testvars import TestVars
from testaid.exceptions import TemplatesResolveError
from testaid.exceptions import AnsibleRunError


def test_testaid_unit_testvars_is_not_none(
        moleculebook,
        jsonvars,
        resolve_vars,
        gather_facts,
        extra_vars):
    with pytest.raises(AnsibleRunError):
        TestVars(moleculebook,
                 jsonvars,
                 resolve_vars,
                 gather_facts,
                 extra_vars).get_testvars()


def test_testaid_unit_testvars_no_resolve_vars(
        moleculebook,
        jsonvars):
    resolve_vars = False
    gather_facts = False
    extra_vars = ''
    testvars = TestVars(moleculebook,
                        jsonvars,
                        resolve_vars,
                        gather_facts,
                        extra_vars).get_testvars()
    assert 'inventory_hostname' in testvars
