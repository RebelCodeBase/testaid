##############################
testaid fixtures for testinfra
##############################

About
=====

With the pytest_ plugin testinfra_ you can write unit tests in python to test
your servers configured by the management tool ansible_. testinfra is the
default verifier_ of the molecule_ testing environment.

The pytest plugin testaid_ provides helper functions and fixtures to facilitate
the use of testinfra. It helps to not only unit test your ansible roles but to
integration and system test your whole ansible project.

.. _pytest: https://pytest.org/
.. _testinfra: https://testinfra.readthedocs.io/en/latest/
.. _ansible: https://www.ansible.com/
.. _verifier: https://molecule.readthedocs.io/en/stable/configuration.html#testinfra
.. _molecule: https://molecule.readthedocs.io/
.. _testaid: https://github.com/RebelCodeBase/testaid

License
=======

`Apache License 2.0 <https://github.com/RebelCodeBase/testaid/blob/master/LICENSE>`_

Quick start
===========

Install the testaid plugin_ using pip_::

    $ pip install testaid

.. _plugin: https://pypi.org/project/testaid/
.. _pip: https://packaging.python.org/tutorials/installing-packages/

Tests
=====

Run ``molecule test`` by invoking tox_::

    $ tox

.. _tox: https://tox.readthedocs.io/en/latest/index.html#

Example
========

Have a look at *test/debian* for a complete example of a molecule project
using ansible, testinfra and testaid.
The molecule project doubles as a test for the testaid plugin.

Boilerplate
===========

As a boilerplate for testinfra tests it is enough to do:

.. code-block:: python

    import testaid

    testinfra_hosts = testaid.hosts()

Fixture testpass
================

You can access gopass_ secrets by using the testpass fixture:

.. code-block:: python

    def test_mytest(host, testpass):

        my_password = testpass('my_project/my_password')

.. _gopass: https://www.gopass.pw/

Fixture testvars
================

Arguably the most useful feature of the testaid plugin is the testvars fixture.
The fixture exposes and resolves the multiple vars files as a python dict:

.. code-block:: python

    def test_mytest(host, testvars):

        my_password = testpass['my_variable']

The following variables are read respecting the ansible variable precedence_:

- ansible setup_ module: ansible_facts
- roles: defaults/main.yml
- testinfra: host.get_variables()
- project: vars/*.yml
- roles: vars/main.yml
- extra vars from TESTAID_EXTRA_VARS_FILES

The TESTAID_EXTRA_VARS_FILES environment variable can be set in molecule.yml.
It can contain relative filepaths to the MOLECULE_SCENARIO_DIRECTORY separated
by colons:

.. code-block:: yaml

    verifier:
      name: testinfra
      options:
        p: cacheprovider
      env:
        TESTAID_EXTRA_VARS_FILES: "../../extra_vars/my_extra_vars.yml:my_molecule_vars.yml"

Internally, the fixture uses the ansible debug_ module to resolve templates.
Thus, it can resolve any kind of template that the debug module can resolve
including jinja2_ code and invoking lookup_ plugins.

As resolving the templates is very slow the fixture will cache the results
using the pytest cache_ plugin if it is enabled.
The plugin is disabled by testinfra by default
and must be explicitly enabled through the ``p: cacheprovider`` option in
*molecule.yml*, see above.
The caching mechanism allows fast test-driven development
but remember to clear the cache when you add or change an ansible variable::

    pytest --cache-clear; molecule verify

The cache will use the molecule ephemeral directory as the cache key which
is unique for each molecule instance.
When using the boilerplate you can inspect the cache by running::

    pytest --cache-show

.. _debug: https://docs.ansible.com/ansible/latest/modules/debug_module.html
.. _precedence: https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable
.. _setup: https://docs.ansible.com/ansible/latest/modules/setup_module.html
.. _jinja2: http://jinja.pocoo.org/
.. _lookup: https://docs.ansible.com/ansible/latest/plugins/lookup.html
.. _cache: https://docs.pytest.org/en/latest/cache.html
