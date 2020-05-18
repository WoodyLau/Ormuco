========
Overview
========

To run, run 
::

    python OverlappingLines.py --first 1 5 --second 6 8
    
Or just
::
    
    python OverlappingLines.py
    
Where it will ask you for the points of the lines to compare.

It will give True if the lines overlap, or False if the lines do not overlap.

This assumes that the versions are alphanumeric, and has the form of digits optionally followed by letters, or just letters.

Project
=======

The goal of this question is to write a program that accepts two lines (x1,x2) and (x3,x4) on the x-axis and returns whether they overlap. As an example, (1,5) and (2,6) overlaps but not (1,5) and (6,8).

Tests
=====

To run the tests, run
::

    python tests.py