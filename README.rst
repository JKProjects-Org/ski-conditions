Ski Conditions  |Travis|_ |Codecov|_
====================================
.. |Travis| image:: https://travis-ci.org/JKProjects-Org/ski-conditions.svg?branch=master
.. _Travis: https://travis-ci.org/JKProjects-Org/ski-conditions

.. |Codecov| image:: https://codecov.io/gh/JKProjects-Org/ski-conditions/branch/master/graph/badge.svg
.. _Codecov: https://codecov.io/gh/JKProjects-Org/ski-conditions


Getting Started
---------------
You can quickly get up and running with the included `Docker <https://www.docker.com/>`_ configuration.

1. Build the Docker container::

    make docker.build

2. Run the service locally, along with Nginx and PostgreSQL::

    make local.up


When running the service with this command, it will be configured to run using the code on your local machine,
rather than the code built in the previous step. Additionally, the `gunicorn <https://gunicorn.org/>`_ application
server has been configured to automatically reload when code is changed locally.

3. If you need to run commands inside the container, you can open a shell with the following command::

    make local.shell

If you would prefer not to use Docker, the project can also be run directly on your machine using
`pipenv <https://pipenv.readthedocs.io/en/latest/>`_. If you develop in this manner, you will be responsible for (a) installing
``pipenv`` and (b) configuring PostgreSQL.

1. Install the requirements::

    make requirements

2. Start Django::

    DEBUG=true SECRET_KEY=replace-me DATABASE_URL=psql://<db-user>:<db-password>@<db-host>:<db-port>/<db-name> python manage.py runserver


Deployment
----------
This project is automatically deployed via Heroku.
