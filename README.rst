================================
Open source django short url app
================================

.. image:: https://travis-ci.org/lefterisnik/django-shorturl.png?branch=master
    :target: https://travis-ci.org/lefterisnik/django-shorturl

A django short URL app.

Requirements
------------

Short URL app requires:

* Python 2.7
* Django version 1.8
* python-social-auth

Quickstart
----------

1. To install this package with virtualenv follow the above instructions::

    mkdir project_name
    cd project_name
    virtualenv env
    source env/bin/activate
    pip install https://github.com/lefterisnik/django-shorturl/archive/master.zip
    django-admin startproject myproject
    cd myproject

2. Add `shorturl` and `so` to your INSTALLED_APPS setting at settings.py file like this::

    INSTALLED_APPS = (
        ...
        'social.apps.django_app.default',
        'shorturl',
    )


3. Add the above to the context proccessor setting::

    ...
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    ...


4. Add your google app key and secret and define the above scopes::

    SOCIAL_AUTH_GOOGLE_PLUS_KEY = ''
    SOCIAL_AUTH_GOOGLE_PLUS_SECRET = ''

    SOCIAL_AUTH_GOOGLE_PLUS_SCOPE = [
        'https://www.googleapis.com/auth/plus.login',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]

  To function properly you must go to Google Developers Console and create credentials and enable Google+ API.

5. Include the shortul URLconf in your project urls.py like this::

    url(r'^', include('shorturl.urls')),

6. Migrate and run server

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver


Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage
