#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input --clear
python manage.py migrate

python manage.py shell << EOF
import os
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created:", username)

domain = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if domain:
    site, _ = Site.objects.get_or_create(id=1)
    site.domain = domain
    site.name = 'Onileayo Agrovet'
    site.save()
    print("Site domain set to:", domain)

client_id = os.environ.get('GOOGLE_CLIENT_ID')
client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
if client_id and client_secret:
    app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={'name': 'Google', 'client_id': client_id, 'secret': client_secret}
    )
    if not created:
        app.client_id = client_id
        app.secret = client_secret
        app.save()
    if domain:
        site = Site.objects.get(id=1)
        app.sites.add(site)
    print("Google sign-in configured")
EOF
