#!/usr/bin/bash

sed -i 's/\[]/\["IP"]/' /home/ubuntu/django-ci/core/settings.py

python manage.py migrate
python manage.py makemigrations
python manage.py collectstatic
sudo service gunicorn restart
sudo service nginx restart
