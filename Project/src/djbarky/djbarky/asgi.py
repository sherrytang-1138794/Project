"""
ASGI config for djbarky project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ChannelNameRouter, ProtocolTypeRouter
from django.core.asgi import get_asgi_application

from barkyapi import consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djbarky.settings")

barky_asgi_app = get_asgi_application()

# for channels support
application = ProtocolTypeRouter(
    {
        "http": barky_asgi_app,
        "channel": ChannelNameRouter(
            {
                "patients-add": consumers.SimplePatientConsumer.as_asgi(),
                "appointments-add": consumers.SimpleAppointmentConsumer.as_asgi(),
                "patient-histories-add": consumers.SimplePatientHistoryConsumer.as_asgi(),
            }
        ),
    }
)
