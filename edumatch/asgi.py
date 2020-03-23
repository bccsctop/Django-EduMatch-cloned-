"""
ASGI config for edumatch project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django
from channels.layers import get_channel_layer
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumatch.settings')
django.setup()
channel_layer = get_channel_layer()
application = get_default_application()