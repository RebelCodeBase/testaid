##############################
Testaid fixtures for testinfra
##############################

About
=====

With the Pytest_ plugin Testinfra_ you can write unit tests in Python to test
your servers configured by the management tool Ansible_. Testinfra is the
default verifier_ of Molecule_ testing environment.

The Pytest plugin Testaid_ provides helper functions and fixtures to facilitate
the use of Testinfra. It helps to not only unit test your Ansible roles but to
integration and system test your whole Ansible project.

.. _Pytest: https://pytest.org/
.. _Testinfra: https://testinfra.readthedocs.io/en/latest/
.. _Ansible: https://www.ansible.com/
.. _verifier: https://molecule.readthedocs.io/en/stable/configuration.html#testinfra
.. _Molecule: https://molecule.readthedocs.io/
.. _Testaid: https://github.com/RebelCodeBase/testaid

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

Run molecule test by invoking tox_::

    $ tox

.. _tox: https://tox.readthedocs.io/en/latest/index.html#

Examples
========

Have a look at test/debian for a complete molecule example using ansible, testinfra and testaid.