import testaid

testinfra_hosts = testaid.hosts()


def test_templates_resolve_template(host, testvars):
    assert testvars['var1'] == 'my_string_1'


def test_templates_resolve_template_transitive(host, testvars):
    assert testvars['var3'] == 'my_string_1'


def test_templates_resolve_template_inline(host, testvars):
    assert testvars['var4'] == 'my_string_1+inline'
