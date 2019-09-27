####################################################
testaid fixtures for ansible, molecule and testinfra
####################################################

About
=====

With the pytest_ plugin testinfra_ you can write unit tests in python to test
your servers configured by the management tool ansible_. testinfra is the
default verifier_ of the molecule_ testing environment.

The pytest plugin testaid_ provides helper functions and fixtures to facilitate
the use of testinfra. It helps to not only unit test your ansible roles but to
integration and system test your whole ansible project.

testinfra wraps cli_ calls to the ansible executable.
testaid uses the ansible python api_ to run ansible playbooks.

.. _pytest: https://pytest.org/
.. _testinfra: https://testinfra.readthedocs.io/en/latest/
.. _ansible: https://www.ansible.com/
.. _verifier: https://molecule.readthedocs.io/en/stable/configuration.html#testinfra
.. _molecule: https://molecule.readthedocs.io/
.. _testaid: https://github.com/RebelCodeBase/testaid
.. _cli: https://philpep.org/blog/infrastructure-testing-with-testinfra
.. _api: https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html

Outline
=======

.. contents:: Table of contents

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

Run unit tests (``pytest``) and system tests (``molecule test``) by invoking tox_::

    $ tox

.. _tox: https://tox.readthedocs.io/en/latest/index.html#

Example
========

Have a look at debian_ system test directory for an example
of a molecule project using ansible, testinfra and testaid.
The molecule project doubles as as a system test
(`golden master`_) for the testaid plugin.

.. _debian: https://github.com/RebelCodeBase/testaid/tree/master/test/system/debian
.. _golden master: https://github.com/supernelis/workshop-renovating-legacy-codebase

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
The fixture resolves and exposes ansible variables as a python dict:

.. code-block:: python

    def test_mytest(host, testvars):

        my_variable = testvars['my_variable']

testvars runs a playbook against the molecule host using the ansible python api.

testvars creates a symbolic link to the roles directory of your ansible project
in the ephemeral playbook environment which molecule sets up.
It then runs a playbook with ``gather_facts:true`` and a debug_ task to get
the ansible variables and the ansible facts of the play and host.

testvars uses the ansible VariableManager_
so the usual ansible variable precedence_ rules apply.
Internally, the fixture uses the ansible debug_ module to resolve templates.
Thus, it can resolve any kind of template that the debug module can resolve
including jinja2_ code and calls to lookup_ plugins.

.. _debug: https://docs.ansible.com/ansible/latest/modules/debug_module.html
.. _VariableManager: https://github.com/ansible/ansible/blob/93ea9612057d47b28c9c42d439ef5679351b762b/lib/ansible/vars/manager.py#L74
.. _precedence: https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable
.. _setup: https://docs.ansible.com/ansible/latest/modules/setup_module.html
.. _jinja2: http://jinja.pocoo.org/
.. _lookup: https://docs.ansible.com/ansible/latest/plugins/lookup.html

extra vars
----------

The ``TESTVARS_EXTRA_VARS`` environment variable can be set in *molecule.yml*.
It can contain dirpaths or filepaths relative to the
``MOLECULE_SCENARIO_DIRECTORY`` separated by colons:

.. code-block:: yaml

    verifier:
      name: testinfra
      env:
        TESTVARS_EXTRA_VARS: "../../vars:../../extra_vars/extra_vars.yml"

The vars files will be included in moleculebook playbooks by adding
the paths to ``vars_files`` (and not by adding ``include_vars`` tasks).

roles
-----

Which roles are included is determined in this order:

- List of roles separated by colon specified in the
  ``TESTVARS_ROLES_WHITELIST`` environment variable
- List of roles specified in playbook speciied in ``molecule.yml``
- List of roles specified in default playbook ``converge.yml``
- All roles in ``roles`` directory in project directory

Roles blacklisted in ``TESTVARS_ROLES_BLACKLIST`` won't be included.

options
-------
testvars is a session scope fixture so its configuration is done in
*molecule.yml* by using pytest command line options.
You can add a couple of options in the options dictionary
of the verifier section:

.. code-block:: yaml

    verifier:
      name: testinfra
      options:
        testvars-no-gather-facts: true

By default, testvars runs a playbook against the molecule host
to gathers ansible variables and facts.
It then runs a playbook against localhost to resolve the variables.

You can change the default behaviour with these options:

- ``testvars-no-gather-facts``
    Run playbook to gather variables with ``gather_facts: false``.
    You won't be able to access ``ansible_facts``
    but your tests will run faster.
- ``testvars-no-gatherfrom-moleculehost``
    Do not gather variables from molecule host.
    Read variables directly from disk without running a playbook.
    It's faster but there is no inventory involved
    so e.g. groups won't work.
- ``testvars-no-resolve-vars``
    Do not resolve any jinja2 template.
    This option might speed up some (unit) tests.
    Implies ``testvars-no-gather-facts``,
    ``testvars-no-gather-molecule`` and ``testvars-no-extra-vars``.
- ``testvars-no-gather-molecule``
    Do not resolve molecule variables.
    You probably won't need these variables
    but it won't take much time to resolve them, either.
- ``testvars-no-extra-vars``
    Do not add extra variables specified in ``TESTVARS_EXTRA_VARS``.
    Ignores the environment variable.
- ``testvars-no-resolvevia-localhost``
    Do not resolve variables against localhost.
    Resolve against molecule host instead.
    This option is only a fallback in case of unknown bugs.

caching
-------

Hopefully the testvars fixture allows fast test-driven development.
It has `session` scope so variables are collected and resolved only once
per testrun as pytest caches the result.
If this is still too slow for you then you can enable the pytest cache_ plugin
in *molecule.yml*:

.. code-block:: yaml

    verifier:
      name: testinfra
      options:
        p: cacheprovider

You should use the testaid boilerplate code to be able to run pytest directly.
Otherwise testinfra will complain about missing environment variables.

Remember to clear the cache when you add or change an ansible variable::

    pytest --cache-clear; molecule verify

The cache will use the molecule ephemeral directory as the cache key which
is unique for each molecule instance.
When using the boilerplate you can inspect the cache by running::

    pytest --cache-show

.. _cache: https://docs.pytest.org/en/latest/cache.html

Ansible Python API
==================

The testaid plugin provides four main pytest fixtures
(and a couple of command line, environment variables and helper fixtures):

- testpass - exposes the ansible passwordstore_ plugin
- testvars - resolves and exposes ansible vars and facts
- moleculebook - api to run playbooks against a molecule host
- moleculeplay - api to leverage the ansible python api

The testvars and testpass fixtures use the moleculebook fixture which in turn
uses the moleculeplay fixture. moleculeplay makes low-level calls to the
`ansible python api`_ and uses the moleculeenv fixture to
handle the sysadmin tasks of setting the right symlinks.
moleculeplay and moleculeenv will probably not be very useful on their own
but moleculebook might be handy in those situations where you know you
shouldn't implement a hackaround. ;-)

Here is how you could run an ansible playbook programmatically from 
a test (or even better: from a fixture_) using dependency injection.

.. code-block:: python

    def test_testaid_moleculebook(host, moleculebook):
        playbook = moleculebook.get()
        args = dict(path='/tmp/moleculebook_did_this', state='touch')
        task_touch = dict(action=dict(module='file', args=args))
        playbook['tasks'].append(task_touch)
        moleculebook.set(playbook)
        moleculebook.run()
        assert host.file('/tmp/moleculebook_did_this').exists

.. _passwordstore: https://docs.ansible.com/ansible/latest/plugins/lookup/passwordstore.html
.. _ansible python api: https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html
.. _fixture: https://docs.pytest.org/en/latest/fixture.html
