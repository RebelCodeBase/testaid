import json
import testaid

testinfra_hosts = testaid.hosts()


def test_testaid_system_templates_resolve_template_string(host,
                                                          testvars):
    assert testvars['my_var_1'] == 'my_string_1'


def test_testaid_system_templates_resolve_template_string(host,
                                                          testvars):
    assert testvars['template1'] == 'my_string_1'


def test_testaid_system_templates_resolve_template_string_transitive(host,
                                                                     testvars):
    assert testvars['template2'] == 'my_string_1'


def test_testaid_system_templates_resolve_template_string_transitive(host,
                                                                     testvars):
    assert testvars['template3'] == 'my_string_1'


def test_testaid_system_templates_resolve_template_string_inline_front(host,
                                                                       testvars):
    assert testvars['template4'] == 'inline+my_string_1'


def test_testaid_system_templates_resolve_template_string_inline_back(host,
                                                                      testvars):
    assert testvars['template5'] == 'my_string_1+inline'


def test_testaid_system_templates_resolve_template_string_inline_both(host,
                                                                      testvars):
    assert testvars['template6'] == 'inline+my_string_1+inline'


def test_testaid_system_templates_resolve_template_no_string(host,
                                                          testvars):
    assert testvars['my_var_2'] == 99


def test_testaid_system_templates_resolve_template_no_string_transitive(host,
                                                                        testvars):
    assert testvars['template7'] == 99


def test_testaid_system_templates_resolve_template_no_string_transitive(host,
                                                                        testvars):
    assert testvars['template8'] == 99


def test_testaid_system_templates_resolve_template_no_string_inline_front(host,
                                                                       testvars):
    assert testvars['template9'] == 'inline+99'


def test_testaid_system_templates_resolve_template_no_string_inline_back(host,
                                                                      testvars):
    assert testvars['template10'] == '99+inline'


def test_testaid_system_templates_resolve_template_no_string_inline_both(host,
                                                                      testvars):
    assert testvars['template11'] == 'inline+99+inline'


def test_testaid_system_templates_resolve_template_special_chars_1(host,
                                                                   testvars):
    assert testvars['special1'] == "äö(ü'!)§$;~é"


def test_testaid_system_templates_resolve_template_special_chars_2(host,
                                                                   testvars):
    assert testvars['special2'] == 'ñô‰(„}»")¯]¿¬'


def test_testaid_system_template_resolve_lookup(host,
                                                testvars):
    assert testvars['lookup_flattened'] == [1, 2, 3, 4, 5, 6]


def test_testaid_system_templates_resolve_template_list(host,
                                                        testvars):
    list1_json = '["first_list_item", "second_list_item"]'
    assert json.dumps(testvars['list1']) == list1_json


def test_testaid_system_templates_resolve_template_nested_list(host,
                                                               testvars):
    list2_json = '["first_list_item", "second_list_item"]'
    assert isinstance(testvars['list2'], list)
    assert json.dumps(testvars['list2']) == list2_json


def test_testaid_system_templates_resolve_template_dict(host,
                                                        testvars):
    dict1_json = '{"first_key": "first_value", "second_key": "second_value"}'
    assert json.dumps(testvars['dict1']) == dict1_json


def test_testaid_system_templates_resolve_template_filter_zip(host,
                                                              testvars):
    filter_zip_json = '[["first_list_item", "anarchism"], '
    filter_zip_json += '["second_list_item", "fortune-anarchism"]]'
    # FIXME: shouldn't this be a list of lists?
    assert json.dumps(testvars['filter_zip']) == filter_zip_json


def test_testaid_system_templates_resolve_template_filter_dict2items(host,
                                                                     testvars):
    filter_dict_json = '[{"key": "first_key", '
    filter_dict_json += '"value": "first_value"}, '
    filter_dict_json += '{"key": "second_key", '
    filter_dict_json += '"value": "second_value"}]'
    assert json.dumps(testvars['filter_dict2items']) == filter_dict_json
