"""
This module utilizes the command pattern - https://en.wikipedia.org/wiki/Command_pattern - to 
specify and implement the business logic layer
"""
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from injector import Injector, inject
import pytz

import requests
from django.db import transaction

from barkyapi.models import Appointment, PatientHistory, Patient
from barkyarch.domain.model import DomainAppointment, DomainPatientHistory, DomainPatient


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        raise NotImplementedError("A command must implement the execute method")


class PythonTimeStampProvider:
    def __init__(self):
        self.now = datetime.now(pytz.UTC).isoformat()

class AddPatientCommand(Command):
    """
    Using the django orm and transactions to add a patient
    """

    @inject
    def __init__(self, now: PythonTimeStampProvider = PythonTimeStampProvider()):
        self.now = now

    def execute(self, data: DomainPatient, timestamp=None):
        record = Patient(data.id, data.patient, data.age, data.phone, data.address)
        record.timestamp = self.now

        # again, we skip the ouw with django's transaction management
        with transaction.atomic():
            record.save()


class GetPatientCommand(Command):
    """
    Using the django orm and transactions to add a patient
    """

    def execute(self, data: int, timestamp=None):
        return Patient.objects.get(id=data).to_domain()


class ListPatientsCommand(Command):
    """
    swapping in Django ORM for the database manager
    """

    def __init__(self, order_by="admit_date"):
        self.order_by = order_by

    def execute(self, data=None):
        return Patient.objects.all().order_by(self.order_by)


class DeletePatientCommand(Command):
    """
    Using the django ORM to delete a patient
    """

    def execute(self, data: DomainPatient):
        record = Patient.objects.get(id=data.id)
        with transaction.atomic():
            record.delete()


class EditPatientCommand(Command):
    """
    Using the django ORM to update a patient
    """

    def execute(self, data: DomainPatient):
        record = Patient.update_from_domain(data)
        with transaction.atomic():
            # record.save()
            pass



class AddPatientHistoryCommand(Command):
    """
    Using the django orm and transactions to add a patient history
    """

    @inject
    def __init__(self, now: PythonTimeStampProvider = PythonTimeStampProvider()):
        self.now = now

    def execute(self, data: DomainPatientHistory, timestamp=None):
        record = PatientHistory(data.history_number, data.admit_date, data.symptons, data.department, data.release_date, data.patient_id)
        record.timestamp = self.now

        # again, we skip the ouw with django's transaction management
        with transaction.atomic():
            record.save()


class GetPatientHistoryCommand(Command):
    """
    Using the django orm and transactions to add a patient record
    """

    def execute(self, data: int, timestamp=None):
        return PatientHistory.objects.get(id=data).to_domain()


class ListPatientHistoriesCommand(Command):
    """
    swapping in Django ORM for the database manager
    """

    def __init__(self, order_by="admit_date"):
        self.order_by = order_by

    def execute(self, data=None):
        return PatientHistory.objects.all().order_by(self.order_by)


class DeletePatientHistoryCommand(Command):
    """
    Using the django ORM to delete a patient record
    """

    def execute(self, data: DomainPatientHistory):
        record = PatientHistory.objects.get(history_number=data.history_number)
        with transaction.atomic():
            record.delete()


class EditPatientHistoryCommand(Command):
    """
    Using the django ORM to update a patient reocrd
    """

    def execute(self, data: DomainPatientHistory):
        record = PatientHistory.update_from_domain(data)
        with transaction.atomic():
            # record.save()
            pass


class AddAppointmentCommand(Command):
    """
    Using the django orm and transactions to add a appointment
    """

    @inject
    def __init__(self, now: PythonTimeStampProvider = PythonTimeStampProvider()):
        self.now = now

    def execute(self, data: DomainAppointment, timestamp=None):
        appointment = Appointment(data.id, data.appointment_date, data.appointment_time, data.status, data.patient, data.doctor)
        appointment.timestamp = self.now

        # again, we skip the ouw with django's transaction management
        with transaction.atomic():
            appointment.save()


class GetAppointmentCommand(Command):
    """
    Using the django orm and transactions to add a appointment
    """

    def execute(self, data: int, timestamp=None):
        return Appointment.objects.get(id=data).to_domain()


class ListAppointmentsCommand(Command):
    """
    swapping in Django ORM for the database manager
    """

    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self, data=None):
        return Appointment.objects.all().order_by(self.order_by)


class DeleteAppointmentCommand(Command):
    """
    Using the django ORM to delete a appointment
    """

    def execute(self, data: DomainAppointment):
        appointment = Appointment.objects.get(patient=data.patient)
        with transaction.atomic():
            appointment.delete()


class EditAppointmentCommand(Command):
    """
    Using the django ORM to update a appointment
    """

    def execute(self, data: DomainAppointment):
        appointment = Appointment.update_from_domain(data)
        with transaction.atomic():
            # appointment.save()
            pass

