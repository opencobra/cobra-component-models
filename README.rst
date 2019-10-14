=============================
COBRA Component Models
=============================

.. image:: https://img.shields.io/pypi/v/cobra-component-models.svg
   :target: https://pypi.org/project/cobra-component-models/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/cobra-component-models.svg
   :target: https://pypi.org/project/cobra-component-models/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/cobra-component-models.svg
   :target: https://www.apache.org/licenses/LICENSE-2.0
   :alt: Apache Software License Version 2.0

.. image:: https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg
   :target: https://github.com/opencobra/cobra-component-models/blob/master/.github/CODE_OF_CONDUCT.md
   :alt: Code of Conduct

.. image:: https://img.shields.io/travis/opencobra/cobra-component-models/master.svg?label=Travis%20CI
   :target: https://travis-ci.org/opencobra/cobra-component-models
   :alt: Travis CI

.. image:: https://codecov.io/gh/opencobra/cobra-component-models/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/opencobra/cobra-component-models
   :alt: Codecov

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Black

.. image:: https://readthedocs.org/projects/cobra-component-models/badge/?version=latest
   :target: https://cobra-component-models.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. summary-start

Provide SQLAlchemy ORM and pydantic data models for
SQL storage and serialization of COBRA components such as reactions, compounds,
and compartments. They are loosely modeled after corresponding classes from the
`SBML Level 3 Version 2 <http://sbml.org/Documents/Specifications>`_
specification.  The data models are primarily intended for web services but
other applications may benefit from these, too.

Install
=======

It's as simple as:

.. code-block:: console

    pip install cobra-component-models

Usage
=====

For now please take a look at the various class definitions and test cases to 
understand how to use the provided models.

Copyright
=========

* Copyright © 2019, Moritz E. Beber.
* Copyright © 2018-2019, Institute for Molecular Systems Biology, ETH Zurich.
* Copyright © 2018-2019, Novo Nordisk Foundation Center for Biosustainability,
  Technical University of Denmark.
* Free software distributed under the `Apache Software License 2.0 
  <https://www.apache.org/licenses/LICENSE-2.0>`_.
* Parts of the included codebase are licensed under the MIT license.

.. summary-end
