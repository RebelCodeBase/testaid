=========
Changelog
=========

0.1
===

* Initial version providing testpass and testvars fixtures

0.2
===

* Convert testaid into a pytest plugin
* Add tox configuration
* Add molecule test project for Debian GNU/Linux
* Add boilerplate function for testinfra invocation

0.3
===

* Add example role: anarchism
* Add resolve templates tests
* Add escape special chars tests
* Add resolve lookup plugin test
* Add documentation to README file
* Add makefile

0.4
===

* Read role/vars/main.yml
* Read project vars/*.yml
* Read TESTAID_EXTRA_VARS_FILES

0.5
===

* Use tmp_path fixture
* Add ansible_facts

0.6
===

* Add github issues tests
* Migrate from os.path to pathlib
* Make cache optional

0.7
===

* Major rewrite: migrate to ansible python api
* Don't invoke testinfra 'class' scoped host fixture
* Use pytest fixture scope 'session' for better caching
* Expose ansible_facts
* Missing feature: include extra vars files

0.8
===

* Fix variable type bugs
* Add command line options to control testvars gathering
* Include extra vars (again) as TESTVARS_EXTRA_VARS
* Provide environment variables as fixtures
* Add unit tests
* Refactor TestVars class

0.9
===

* Refactor classes
* Refactor plugins
* Add unit tests

0.10
====
* Almost full unit test coverage

0.11
====
* Gather and resolve against localhost
* Make role inclusion configurable