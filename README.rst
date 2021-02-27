========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis|
        |
        | |codeclimate|
    * - package
      - | |commits-since|

.. |travis| image:: https://api.travis-ci.com/stuartneilson/2021sp-csci-utils-stuartneilson.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/stuartneilson/2021sp-csci-utils-stuartneilson

.. |codeclimate| image:: https://codeclimate.com/github/stuartneilson/2021sp-csci-utils-stuartneilson/badges/gpa.svg
   :target: https://codeclimate.com/github/stuartneilson/2021sp-csci-utils-stuartneilson
   :alt: CodeClimate Quality Status

.. |commits-since| image:: https://img.shields.io/github/commits-since/stuartneilson/2021sp-csci-utils-stuartneilson/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/stuartneilson/2021sp-csci-utils-stuartneilson/compare/v0.0.0...master



.. end-badges

CSCI-Utils pset Spring 2021

Installation
============

::

    pip install csci-utils

You can also install the in-development version with::

    pip install https://github.com/stuartneilson/2021sp-csci-utils-stuartneilson/archive/master.zip


Documentation
=============


To use the project:

.. code-block:: python

    import csci_utils
    csci_utils.longest()


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
