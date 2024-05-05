# python
import asyncio
import datetime
import json

# Django
from channels.consumer import AsyncConsumer, SyncConsumer
from channels.generic.http import AsyncHttpConsumer

# Local
from barkyapi.models import Patient, PatientHistory, Appointment

from django.contrib.auth.models import User #add


class SimplePatientConsumer(AsyncConsumer):
    async def print_patient(self, message):
        print(f"WORKER: Patient: {message['data']}")

class SimplePatientHistoryConsumer(AsyncConsumer):
    async def print_patienthistory(self, message):
        print(f"WORKER: Patient History: {message['data']}")

class SimpleAppointmentConsumer(AsyncConsumer):
    async def print_appointment(self, message):
        print(f"WORKER: Appointment: {message['data']}")

class SimpleUserConsumer(AsyncConsumer):
    async def print_appointment(self, message):
        print(f"WORKER: User: {message['data']}")


# class BookmarkConsumer(AsyncHttpConsumer):
#     async def handle(self, body):
#         # Get all bookmarks
#         bookmarks = Bookmark.objects.all()
#         # Serialize the bookmarks
#         data = json.dumps(
#             [{"title": bookmark.title, "url": bookmark.url} for bookmark in bookmarks]
#         )
#         # Send the serialized data as a JSON response
#         await self.send_response(
#             200, data, headers=[(b"Content-Type", b"application/json")]
#         )

#     # Server-send event https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
#     async def handle(self, body):
#         await self.send_headers(
#             headers=[
#                 (b"Cache-Control", b"no-cache"),
#                 (b"Content-Type", b"text/event-stream"),
#                 (b"Transfer-Encoding", b"chunked"),
#             ]
#         )
#         while True:
#             payload = "data: %s\n\n" % datetime.now().isoformat()
#             await self.send_body(payload.encode("utf-8"), more_body=True)
#             await asyncio.sleep(1)

#     async def send_bookmark(self, bookmark):
#         # Serialize the bookmark
#         data = json.dumps({"title": bookmark.title, "url": bookmark.url})
#         # Send the serialized data as a JSON response
#         await self.channel_layer.send(
#             "bookmarks-add", {"type": "send.bookmark", "data": data}
#         )
#         # await self.send_response(
#         #     200, data, headers=[(b"Content-Type", b"application/json")]
#         # )
