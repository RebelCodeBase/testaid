##############################
Testaid fixtures for testinfra
##############################

About
=====

With the Pytest_ plugin Testinfra_ you can write tests in Python to test your
servers configured by management tools like Ansible_, Salt_, Puppet_ or Chef_.

Although Testinfra was originally designed for unit tests it can be used for
integration and system tests when used as a verifier_ for Molecule_.
In this case Testaid provides helpful Pytest fixtures.

.. _Pytest: https://pytest.org/
.. _Testinfra: https://testinfra.readthedocs.io/en/latest/
.. _Ansible: https://www.ansible.com/
.. _Salt: https://saltstack.com/
.. _Puppet: https://puppetlabs.com/
.. _Chef: https://www.chef.io/
.. _verifier: https://molecule.readthedocs.io/en/stable/configuration.html#testinfra
.. _Molecule: https://molecule.readthedocs.io/

License
=======

`Apache License 2.0 <https://github.com/RebelCodeBase/testaid/blob/master/LICENSE>`_

Quick start
===========

Install testaid using pip::

    $ pip install testaid
