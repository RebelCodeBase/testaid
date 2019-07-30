
#from ruamel.yaml import YAML
#import sys
import testaid

testinfra_hosts = testaid.hosts()
#yaml = YAML()

# issue: https://github.com/RebelCodeBase/testaid/issues/1
# needs: https://github.com/philpep/testinfra/pull/462
# def test_testaid_github_issues_1_001(testvars):
#    assert testvars['github_issues_1_file'] == 'bar'

# issue: https://github.com/RebelCodeBase/testaid/issues/1
# print testvars as yaml
#def test_testaid_github_issues_1_002(testvars):
#    yaml.dump(testvars, sys.stdout)
#    assert False