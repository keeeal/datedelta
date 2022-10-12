Usage
=====

Command Line Interface
----------------------

DateDelta is a command line tool which accepts two date string arguments. The
program will compute the number of days between the two dates provided, print
the result, and exit.

The date strings must be provided in
`isoformat <https://en.wikipedia.org/wiki/ISO_8601#Dates>`_, specifically in
the form ``YYYY-MM-DD``.

.. code-block:: none

   usage: datedelta [-h] [-i] [date_strings ...]

   positional arguments:
     date_strings

   optional arguments:
     -h, --help         show this help message and exit
     -i, --interactive

For example:

.. code-block:: console

   $ datedelta 2012-01-10 2012-01-11
   0

.. code-block:: console

   $ datedelta 2021-12-01 2017-12-14
   1447

Interactive Mode
----------------

DateDelta can be started in interactive mode using the ``-i`` flag.

In interactive mode, pairs of dates can be provided on the same line and the
difference will be displayed. Type ``exit`` to close the interactive session.

For example:

.. code-block:: console

   $ datedelta -i                                                     py hai
   2012-01-10 2012-01-11
   0
   2021-12-01 2017-12-14
   1447
   exit

Incomplete or malformed input during interactive mode will result in an error
message and the program will exit.

Python Package
--------------

DateDelta can be used as a Python package. At the core of DateDelta is the Date
class.

.. code-block:: python

   from datedelta import Date

Date classes can be initialized directly in the same way as Python's built-in
``datetime.date`` class.

.. code-block:: python

   Date(2012, 1, 10) - Date(2012, 1, 11)  # => 0
   Date(2021, 12, 1) - Date(2017, 12, 14)  # => 1447

For more details, the API can be found :doc:`here<api>`.
