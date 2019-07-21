import json
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
    expected = os.environ['HOME']
    assert re.search(expected, testvars['lookup1']) is not None


def test_testaid_templates_resolve_template_list(testvars):
    list1_json = '["first_list_item", "second_list_item"]'
    assert json.dumps(testvars['list1']) == list1_json


def test_testaid_templates_resolve_template_dict(testvars):
    dict1_json = '{"first_key": "first_value", "second_key": "second_value"}'
    assert json.dumps(testvars['dict1']) == dict1_json


def test_testaid_templates_resolve_template_filter_zip(testvars):
    filter_zip_json = '"[[\'first_list_item\', \'anarchism\'], '
    filter_zip_json += '[\'second_list_item\', \'fortune-anarchism\']]"'
    assert json.dumps(testvars['filter_zip']) == filter_zip_json


def test_testaid_templates_resolve_template_filter_dict2items(testvars):
    filter_dict_json = '"[{\'key\': \'first_key\', '
    filter_dict_json += '\'value\': \'first_value\'}, '
    filter_dict_json += '{\'key\': \'second_key\', '
    filter_dict_json += '\'value\': \'second_value\'}]"'
    assert json.dumps(testvars['filter_dict2items']) == filter_dict_json
