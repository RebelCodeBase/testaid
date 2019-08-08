# import mock
import testaid

testinfra_hosts = testaid.hosts()

# @mock.patch('testaid.moleculebook.MoleculeBook.run',
#             return_value=[{'msg':'my_secret_value'}])
# def test_testaid_testpass_mock(host, testpass):
#      my_secret_value = testpass('my_secret_key')
#      assert my_secret_value == 'my_secret_value'


def test_testaid_testpass_monkeypatch(host, monkeypatch, testpass):
    monkeypatch.setattr(testaid.moleculebook.MoleculeBook, 'run',
                        lambda x: [{'msg': 'my_secret_value'}])
    my_secret_value = testpass('my_secret_key')
    assert my_secret_value == 'my_secret_value'
