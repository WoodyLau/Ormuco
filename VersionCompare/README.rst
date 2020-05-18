========
Overview
========

To run, run 
::

    python VersionCompare.py --first 1.22.1a --second 1.1.3
    
Or just
::
    
    python VersionCompare.py
    
Where it will ask you for the two versions to compare.

It will give 1 if the first has a greater version than the second, 0 if they are equal, and -1 if it has a lower version.

This assumes that the versions are alphanumeric, and has the form of digits optionally followed by letters, or just letters.

Project
=======

The goal of this question is to write a software library that accepts 2 version string as input and
returns whether one is greater than, equal, or less than the other. As an example: “1.2” is
greater than “1.1”.

Tests
=====

To run the tests, run
::

    python tests.py