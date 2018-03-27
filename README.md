# uniqid
Project repository of my bachelors project creating an application
to help autistic people communicate about what autism means to them

## installation
Install the project and its dependencies in a virtualenv

    git clone https://github.com/aspigirlcodes/uniqid.git
    cd uniqid/
    python3 -m venv uniqid-venv
    source uniqid-venv/bin/activate
    pip install -r requirements.txt

Setup postgres database

    sudo su - postgres
    psql
    #in postgresql prompt
    CREATE DATABASE myproject;
    CREATE USER myprojectuser WITH PASSWORD 'password';
    ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
    ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE myprojectuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
    \q
    # exist postgres user session
    exit

add local settings file

    cp uniqid/settings_local.py.template uniqid/settings_local.py

And fill in the database name, user and password you've set up earlier,
set HOST = 'localhost'

Add a secret key and set the debug boolean according to your preferences.

Setup Project

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser

Running the tests

    python manage.py test

Running the development server

    python manage.py runserver

## Versions and version control

master is the production branch, dev is the development branch.
Tags on master indicate the different releases.
The last release is tagged 'v0.5'
