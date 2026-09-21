"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# WhiteNoise serves collected static files and the property photos under
# resources/media, so gunicorn needs no separate file server in front of it.
# The photos are committed to the repo, not user uploads, so serving them
# like static assets is safe.
application = WhiteNoise(get_wsgi_application(), root=settings.STATIC_ROOT, prefix=settings.STATIC_URL)
application.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)
