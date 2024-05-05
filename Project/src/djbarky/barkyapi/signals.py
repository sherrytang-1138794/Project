import csv
from pathlib import Path
from random import randint

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.core.files import File
from django.db.models.signals import post_save

from .consumers import SimplePatientConsumer, SimplePatientHistoryConsumer, SimpleAppointmentConsumer, SimpleUserConsumer
from .models import Patient, PatientHistory, Appointment

from django.contrib.auth.models import User #add

channel_layer = get_channel_layer()


# making sense of this example:
# - save_bookmark is the receiver function
# - Bookmark is the sender and post_save is the signal.
# - Use Case: Everytime a Bookmark is saved, the save_profile function will be executed.
def log_patient_to_csv(sender, instance, **kwargs):
    print("Patient signal: CSV")

    file = Path(__file__).parent.parent / "barkyarch" / "domain" / "patient_log.csv"
    print(f"Writing to {file}")

    # the with statement takes advantate of the context manager protocol: https://realpython.com/python-with-statement/#the-with-statement-approach
    # for reference, here is how open() works: https://docs.python.org/3/library/functions.html#open
    with open(file, "a+", newline="") as csvfile:
        logfile = File(csvfile)
        logwriter = csv.writer(
            logfile,
            delimiter=",",
        )
        logwriter.writerow(
            [
                instance.id,
                instance.patient,
                instance.age,
                instance.phone,
                instance.address,
            ]
        )

def log_patient_history_to_csv(sender, instance, **kwargs):
    print("Patient History signal: CSV")

    file = Path(__file__).parent.parent / "barkyarch" / "domain" / "patient_history_log.csv"
    print(f"Writing to {file}")

    # the with statement takes advantate of the context manager protocol: https://realpython.com/python-with-statement/#the-with-statement-approach
    # for reference, here is how open() works: https://docs.python.org/3/library/functions.html#open
    with open(file, "a+", newline="") as csvfile:
        logfile = File(csvfile)
        logwriter = csv.writer(
            logfile,
            delimiter=",",
        )
        logwriter.writerow(
            [
                instance.history_number,
                instance.admit_date,
                instance.symptons,
                instance.department,
                instance.release_date,
                instance.patient_id
            ]
        )

def log_appointment_to_csv(sender, instance, **kwargs):
    print("Patient History signal: CSV")

    file = Path(__file__).parent.parent / "barkyarch" / "domain" / "patient_appointment_log.csv"
    print(f"Writing to {file}")

    # the with statement takes advantate of the context manager protocol: https://realpython.com/python-with-statement/#the-with-statement-approach
    # for reference, here is how open() works: https://docs.python.org/3/library/functions.html#open
    with open(file, "a+", newline="") as csvfile:
        logfile = File(csvfile)
        logwriter = csv.writer(
            logfile,
            delimiter=",",
        )
        logwriter.writerow(
            [
                instance.id,
                instance.appointment_date,
                instance.appointment_time,
                instance.status,
                instance.patient,
                instance.doctor,
            ]
        )

def log_user_to_csv(sender, instance, **kwargs):
    print("User signal: CSV")

    file = Path(__file__).parent.parent / "barkyarch" / "domain" / "user_log.csv"
    print(f"Writing to {file}")

    # the with statement takes advantate of the context manager protocol: https://realpython.com/python-with-statement/#the-with-statement-approach
    # for reference, here is how open() works: https://docs.python.org/3/library/functions.html#open
    with open(file, "a+", newline="") as csvfile:
        logfile = File(csvfile)
        logwriter = csv.writer(
            logfile,
            delimiter=",",
        )
        logwriter.writerow(
            [
                instance.id,
                instance.username,
                instance.password,
            ]
        )


def send_patient_to_channel(sender, instance, **kwargs):
    print("Patient signal: Channel")
    print(f"Sending patient to channel: {instance}")

    async_to_sync(channel_layer.send)(
        "patients-add", {"type": "print.patient", "data": instance.patient}
    )

def send_patient_history_to_channel(sender, instance, **kwargs):
    print("Patient History signal: Channel")
    print(f"Sending patient to channel: {instance}")

    async_to_sync(channel_layer.send)(
        "patient-histories-add", {"type": "print.patienthistory", "data": instance.history_number}
    )

def send_appointment_to_channel(sender, instance, **kwargs):
    print("Patient Appointment signal: Channel")
    print(f"Sending patient to channel: {instance}")

    async_to_sync(channel_layer.send)(
        "appointments-add", {"type": "print.appointment", "data": instance.patient}
    )

def send_user_to_channel(sender, instance, **kwargs):
    print("User signal: Channel")
    print(f"Sending user to channel: {instance}")

    async_to_sync(channel_layer.send)(
        "users-add", {"type": "print.user", "data": instance.username}
    )


# connect the signal to this receiver
post_save.connect(log_patient_to_csv, sender=Patient)
post_save.connect(send_patient_to_channel, sender=Patient)

post_save.connect(log_patient_history_to_csv, sender=PatientHistory)
post_save.connect(send_patient_history_to_channel, sender=PatientHistory)

post_save.connect(log_appointment_to_csv, sender=Appointment)
post_save.connect(send_appointment_to_channel, sender=Appointment)

post_save.connect(log_user_to_csv, sender=User)
post_save.connect(send_user_to_channel, sender=User)
