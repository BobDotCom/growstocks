:github_url: https://github.com/BobDotCom/growstocks

.. currentmodule:: growstocks

API Reference
===============

The following section outlines the API of the growstocks package.


.. _core_utilities:

Core Utilities
--------------
These provide the main functionality of this package.


Client Class
~~~~~~~~~~~~

.. autoclass:: Client
   :members:

Connection Classes
~~~~~~~~~~~~~~~~~~

.. autoclass:: Pay
   :members:

.. autoclass:: Auth
   :members:


.. _object_classes:

Object Classes
--------------
These classes are returned by various methods from the :ref:`core_utilities`. They represent objects returned by (or to
be sent to) the API.


Scopes Class
~~~~~~~~~~~~

.. autoclass:: Scopes
   :members:

User Class
~~~~~~~~~~

.. autoclass:: User
   :members:

Transaction Class
~~~~~~~~~~~~~~~~~

.. autoclass:: Transaction
   :members:


.. _exceptions:

Exceptions
----------
These are exceptions that can be returned by any function/method in this library.

.. autoclass:: GrowstocksException
   :members:

.. autoclass:: RequestFailure
   :members:

.. autoclass:: RedirectUriNone
   :members:
