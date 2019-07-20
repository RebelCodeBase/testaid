import os
import re
import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_templates_resolve_template(testvars):
    assert testvars['template1'] == 'my_string_1'


def test_testaid_templates_resolve_template_transitive(testvars):
    assert testvars['template3'] == 'my_string_1'


def test_testaid_templates_resolve_template_inline_front(testvars):
    assert testvars['template4'] == 'inline+my_string_1'


def test_testaid_templates_resolve_template_inline_back(testvars):
    assert testvars['template5'] == 'my_string_1+inline'


def test_testaid_templates_resolve_template_special_chars_1(testvars):
    assert testvars['special1'] == "äöü'!)§$;~é"


def test_testaid_templates_resolve_template_special_chars_2(testvars):
    assert testvars['special2'] == 'ñô‰„}»"¯]¿¬'


def test_testaid_template_resolve_lookup(testvars):
    expected = os.environ['USER']
    assert re.search(expected, testvars['lookup1']) is not None
