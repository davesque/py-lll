py-lll
======

An LLL compiler for Python.

LLL (Low-level Lisp-like Language) is a smart contract programming language
for the Ethereum blockchain. It seeks to provide a thin, human-readable layer
over the atomic operations that occur during execution of a smart contract on
the EVM (Ethereum Virtual Machine). LLL is available in various flavors as a
stand-alone language and is also used as an IR (intermediate representation)
during compilation of contracts written in the Vyper smart contract language.
The py-lll project implements the variety of LLL used as an IR by Vyper.

This project is intended to provide the following::

* A compiler for contracts written in LLL
* Documentation of LLL and its features
* A maximally transparent and maintainable implementation of LLL
* A flavor of LLL useful as an IR for higher-level smart contract
  languages

To fulfill these goals, py-lll favors simplicity over expressiveness.

Contents
--------

.. toctree::
    :maxdepth: 3

    lll
    releases


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
