===================
growstocks
===================

A wrapper for the GrowStocks API, made for both synchronous and asynchronous applications.

NOTE: asynchronous support has not been implemented yet, but is planned for the near future.

|Status badge|

.. |Status badge| image:: https://github.com/BobDotCom/growstocks/workflows/Python%20Package/badge.svg
   :target: https://github.com/BobDotCom/growstocks/actions?query=workflow%3A"Python+Package"
   :alt: Package Status

|Docs badge|

.. |Docs badge| image:: https://readthedocs.org/projects/growstocks/badge/?version=latest
   :target: https://growstocks.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

PyPI: https://pypi.org/project/growstocks/

Docs: https://growstocks.readthedocs.io/en/latest/

Installation
############
You can install released versions of growstocks from the Python Package Index via pip or a similar tool:

**Stable Release:** ``pip install growstocks``

**Working Version:** ``pip install git+https://github.com/BobDotCom/growstocks.git``

Usage
#####

.. code-block:: python

    >>> import growstocks
    >>> client = growstocks.Client(913117854995652992,"T%GRD4iEiFmgyYE!O5&ZCx3Rn%uqwPV3")
    >>> client.default_scopes = growstocks.Scopes(profile=True, balance=True, discord=True)
    >>> user = client.auth.fetch_user('31G4k57rG3asdyyi5Lqk')
    >>> dict(user)
    {'discord_id': '690420846774321221',
     'id': 1916,
     'name': 'BobDotCom',
     'email': None,
     'growid': 'Bob430',
     'balance': 3}

Using Async
###########
To use in an async context, just use ``import growstocks.aio as growstocks`` as your import and make sure to await the functions marked as coroutines.

.. code-block:: python

    import growstocks.aio as growstocks