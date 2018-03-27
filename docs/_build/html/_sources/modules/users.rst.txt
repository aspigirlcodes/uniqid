Users app
=============

Introduction
-------------
The users app is responsible for all user account related logic.
It relies heavily on logic provided by django\.contrib\.auth.
However the user's email address is used as a username.
The email address is verified upon registration by sending a token link.
The same kind of token link is also used for reseting the user's password.

Django's user model is also  enhanced by the :class:`users.models.Profile`
model, that can contain extra user related information and is connected to
the user by a one-to-one relationship.

users\.models module
--------------------

.. automodule:: users.models
    :members:
    :show-inheritance:

users\.urls module
------------------

.. automodule:: users.urls
    :members:
    :show-inheritance:

users\.views module
-------------------

.. automodule:: users.views
    :members:
    :show-inheritance:

users\.forms module
-------------------

.. automodule:: users.forms
    :members:
    :show-inheritance:
