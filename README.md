OMERO.qa
========

OMERO.qa is the web application which helps support community by OMERO team.

Requirements
============

* PostgreSQL 8.2+
* Python 2.6+

Development Installation
========================

1. Clone the repository

        git clone git@github.com:openmicroscopy/qa.git

2. Set up a virtualenv (http://www.pip-installer.org/) and activate it

        curl -O -k https://raw.github.com/pypa/virtualenv/master/virtualenv.py
        python virtualenv.py qa-virtualenv
        source qa-virtualenv/bin/activate
        pip install numpy
        pip install -r requirements.txt

3. Download and extract the GeoIP country and city databases

        curl -O http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
        curl -O http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
        gzip -d GeoIP.dat.gz
        gzip -d GeoLiteCity.dat.gz

4. Run tests

        python manage.py test registry --settings=omero_qa.settings-test -v 3

6. Set up your database

        # Create a PostgreSQL user
        sudo -u postgres createuser -P -D -R -S feedback_user
        # Create a database
        sudo -u postgres createdb -O feedback_user feedback


Configuration
=============

* Create new settings_prod.py and import default settings

        from settings import *

* Set `DEBUG`

        DEBUG=False
        TEMPLATE_DEBUG = DEBUG

* Set `ADMINS`

        ADMINS = (
            ('User name', 'email'),
        )

* Change database settings

        ...
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'feedback',                      # Or path to database file if using sqlite3.
        'USER': 'feedback_user',                      # Not used with sqlite3.
        'PASSWORD': 'password',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
        ...

* Modify `FEEDBACK_URL = "qa.openmicroscopy.org.uk:80"` - this is the host where errors should be reported if application itself crashes

* Obtain Google key on http://code.google.com/apis/maps/signup.html optional

* Create rest of required dirs:
    * UPLOAD_ROOT = "/FileStore" <- this is equivalent of /ome/apache_repo
    * VALIDATOR_UPLOAD_ROOT = "/Validator"
    * TESTNG_ROOT = "/TestNG"
 
* Set up `APPLICATION_HOST = "http://qa.openmicroscopy.org.uk"`- this is part of the url what appears in email. When user click it, should jump to the feedback page.

* Set up email server
    
        # Application allows to notify user
        EMAIL_HOST = 'localhost'
        EMAIL_HOST_PASSWORD = ''
        EMAIL_HOST_USER = ''
        EMAIL_PORT = 25
        EMAIL_SUBJECT_PREFIX = '[OMERO.qa] '
        EMAIL_USE_TLS = False
        SERVER_EMAIL = 'A.Tarkowska@dundee.ac.uk' # email address

* Synchronise the database

        export DJANGO_SETTINGS_MODULE=omerostats.settings-prod
        python manage.py syncdb --settings=settings-prod

* Create admin user

         echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell

* Collect statics

        python manage.py collectstatic

Trac systems
============

 * Configure user to create ticket in Trac
 
        trac.openmicroscopy.org.uk/ome

Site 1
======

Login to admin panel and change `Site = 1` to current qa_host qa.openmicroscopy.org.uk.

Legal
=====

The source for OMERO.qa is released under the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OMERO.qa is Copyright (C) 2008-2015 University of Dundee
