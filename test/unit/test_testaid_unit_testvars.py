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
        jsonvars,
        gather_facts,
        extra_vars):
    resolve_vars = False
    testvars = TestVars(moleculebook,
                        jsonvars,
                        resolve_vars,
                        gather_facts,
                        extra_vars).get_testvars()
    assert 'inventory_hostname' in testvars


def test_testaid_unit_testvars_exception_testvarsresolvefailed():
    msg = 'my_msg'
    with pytest.raises(
            TemplatesResolveError,
            match=r'^my_msg$'):
        raise TemplatesResolveError(msg)
