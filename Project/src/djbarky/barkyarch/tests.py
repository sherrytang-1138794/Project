from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import localtime

from barkyapi.models import Patient, PatientHistory, Appointment
from barkyarch.domain.model import DomainPatient, DomainAppointment, DomainPatientHistory
from barkyarch.services.commands import (
    AddPatientCommand,
    GetPatientCommand,
    ListPatientsCommand,
    DeletePatientCommand,
    EditPatientCommand,
    AddPatientHistoryCommand,
    GetPatientHistoryCommand,
    ListPatientHistoriesCommand,
    DeletePatientHistoryCommand,
    EditPatientHistoryCommand,
    AddAppointmentCommand,
    GetAppointmentCommand,
    ListAppointmentsCommand,
    DeleteAppointmentCommand,
    EditAppointmentCommand,
)


class TestPatientCommands(TestCase):
    def setUp(self):
        self.domain_patient_1 = DomainPatient(
            id=1,
            patient="Emily Brown",
            age=34,
            phone="8063492402",
            address="4th Ave, Canyon City, TX79015",
        )

        self.domain_patient_2 = DomainPatient(
            id=2,
            patient="Nina December",
            age=54,
            phone="8063420322",
            address="5th Ave, Canyon City, TX79015",
            
        )

    def test_patient_command_add(self):
        add_command = AddPatientCommand()
        add_command.execute(self.domain_patient_1)

        # run checks
        # one object is inserted
        self.assertEqual(Patient.objects.count(), 1)

        # that object is the same as the one we inserted
        self.assertEqual(Patient.objects.get(id=1).patient, self.domain_patient_1.patient)

    def test_patient_command_edit(self):

        add_command = AddPatientCommand()
        add_command.execute(self.domain_patient_1)

        # using command
        # get_command = GetPatientCommand()
        # domain_patient_temp = get_command.execute(self.domain_patient_1.id)
        # domain_patient_temp.patient = "Nancy Wasington"

        # or just modify
        self.domain_patient_1.patient = "Nancy Washington"

        edit_command = EditPatientCommand()
        edit_command.execute(self.domain_patient_1)

        # run checks
        # one object is inserted
        self.assertEqual(Patient.objects.count(), 1)

        # that object is the same as the one we inserted
        self.assertEqual(Patient.objects.get(id=1).patient, "Nancy Washington")

    def test_patient_command_get(self):
        add_command = AddPatientCommand()
        add_command.execute(self.domain_patient_1)
        add_command.execute(self.domain_patient_2)

        get_command = GetPatientCommand()
        domain_patient_temp = get_command.execute(self.domain_patient_1.id)

        # run checks
        # one object is inserted
        self.assertEqual(Patient.objects.count(), 2)
        self.assertEqual(domain_patient_temp.patient, "Emily Brown")
    

    def test_patient_command_list(self):
        add_command = AddPatientCommand()
        add_command.execute(self.domain_patient_1)
        add_command.execute(self.domain_patient_2)

        list_command = ListPatientsCommand()
        list_command.execute(Patient)

        # run checks
        # one object is inserted
        self.assertEqual(Patient.objects.count(), 2)
        self.assertEqual(Patient.objects.first().patient, "Emily Brown")
    
    def test_patient_command_delete(self):
        add_command = AddPatientCommand()
        add_command.execute(self.domain_patient_1)
        add_command.execute(self.domain_patient_2)

        delete_command = DeletePatientCommand()
        delete_command.execute(self.domain_patient_1)

        # run checks
        # one object is inserted
        self.assertEqual(Patient.objects.count(), 1)
        


class TestPatientHistoryCommands(TestCase):
    def setUp(self):
        self.domain_patient_history_1 = DomainPatientHistory(
            history_number=1,
            admit_date="2024-05-02",
            symptons="fever, Nasal congestant",
            department="EMC",
            release_date="2024-05-03",
            patient_id="1"
        )

        self.domain_patient_history_2 = DomainPatientHistory(
            history_number=2,
            admit_date="2024-05-01",
            symptons="Nasal congestant, Cough",
            department="EMC",
            release_date="2024-05-01",
            patient_id="2"
            
        )

    def test_patient_history_command_add(self):
        add_command = AddPatientHistoryCommand()
        add_command.execute(self.domain_patient_history_1)

        # run checks
        # one object is inserted
        self.assertEqual(PatientHistory.objects.count(), 1)

        # that object is the same as the one we inserted
        self.assertEqual(PatientHistory.objects.get(history_number=1).patient_id, self.domain_patient_history_1.patient_id)

    def test_patient_history_command_edit(self):

        add_command = AddPatientHistoryCommand()
        add_command.execute(self.domain_patient_history_1)

        # using command
        # get_command = GetPatientCommand()
        # domain_patient_temp = get_command.execute(self.domain_patient_1.id)
        # domain_patient_temp.patient = "Nancy Wasington"

        # or just modify
        self.domain_patient_history_1.release_date = "2024-05-02"

        edit_command = EditPatientHistoryCommand()
        edit_command.execute(self.domain_patient_history_1)

        # run checks
        # one object is inserted
        self.assertEqual(PatientHistory.objects.count(), 1)

        # that object is the same as the one we inserted
        self.assertEqual(PatientHistory.objects.get(history_number=1).patient_id, "1")

    def test_patient_history_command_get(self):
        add_command = AddPatientHistoryCommand()
        add_command.execute(self.domain_patient_history_1)
        add_command.execute(self.domain_patient_history_2)

        get_command = GetPatientHistoryCommand()
        domain_patient_temp = get_command.execute(self.domain_patient_history_1.history_number)

        # run checks
        # one object is inserted
        self.assertEqual(PatientHistory.objects.count(), 2)
        self.assertEqual(domain_patient_temp.symptons, "fever, Nasal congestant")
    

    def test_patient_history_command_list(self):
        add_command = AddPatientHistoryCommand()
        add_command.execute(self.domain_patient_history_1)
        add_command.execute(self.domain_patient_history_2)

        list_command = ListPatientHistoriesCommand()
        list_command.execute(PatientHistory)

        # run checks
        # one object is inserted
        self.assertEqual(PatientHistory.objects.count(), 2)
        self.assertEqual(PatientHistory.objects.first().symptons, "fever, Nasal congestant")
    

    def test_patient_history_command_delete(self):
        add_command = AddPatientHistoryCommand()
        add_command.execute(self.domain_patient_history_1)
        add_command.execute(self.domain_patient_history_2)

        delete_command = DeletePatientHistoryCommand()
        delete_command.execute(self.domain_patient_history_1)

        # run checks
        # one object is inserted
        self.assertEqual(PatientHistory.objects.count(), 1)
        


class TestAppointmentCommands(TestCase):
    def setUp(self):
        self.domain_appointment_1 = DomainAppointment(
            id=1,
            appointment_date="2024-05-10",
            appointment_time="13:00:00",
            status=False,
            patient="Iris Patrick",
            doctor="Greeway"
        )

        self.domain_appointment_2 = DomainAppointment(
            id=2,
            appointment_date="2024-05-06",
            appointment_time="15:30:00",
            status=False,
            patient="Nina December",
            doctor="Watson",
        )

    def test_appointment_command_add(self):
        add_command = AddAppointmentCommand()
        add_command.execute(self.domain_appointment_1)

        # run checks
        # one object is inserted
        self.assertEqual(Appointment.objects.count(), 1)

        # that object is the same as the one we inserted
        self.assertEqual(Appointment.objects.get(id=1).patient, self.domain_appointment_1.patient)

    def test_appointment_command_edit(self):

        add_command = AddAppointmentCommand()
        add_command.execute(self.domain_appointment_1)

        # using command
        # get_command = GetPatientCommand()
        # domain_patient_temp = get_command.execute(self.domain_patient_1.id)
        # domain_patient_temp.patient = "Nancy Wasington"

        # or just modify
        self.domain_appointment_1.patient = "Iris Patrick"

        edit_command = EditAppointmentCommand()
        edit_command.execute(self.domain_appointment_1)

        # run checks
        # one object is inserted
        self.assertEqual(Appointment.objects.count(), 1)

        # that object is the same as the one we inserted
        self.assertEqual(Appointment.objects.get(id=1).patient, "Iris Patrick")


    
    def test_appointment_command_get(self):
        add_command = AddAppointmentCommand()
        add_command.execute(self.domain_appointment_1)
        add_command.execute(self.domain_appointment_2)

        get_command = GetAppointmentCommand()
        domain_patient_temp = get_command.execute(self.domain_appointment_1.patient)

        # run checks
        # one object is inserted
        self.assertEqual(Appointment.objects.count(), 2)
        self.assertEqual(domain_patient_temp.patient, "Iris Patrick")
    

    def test_appointment_command_list(self):
        add_command = AddAppointmentCommand()
        add_command.execute(self.domain_appointment_1)
        add_command.execute(self.domain_appointment_2)

        list_command = ListAppointmentsCommand()
        list_command.execute(Appointment)

        # run checks
        # one object is inserted
        self.assertEqual(Appointment.objects.count(), 2)
        self.assertEqual(Appointment.objects.first().patient, "Iris Patrick")
    

    def test_appoint_command_delete(self):
        add_command = AddAppointmentCommand()
        add_command.execute(self.domain_appointment_1)
        add_command.execute(self.domain_appointment_2)

        delete_command = DeleteAppointmentCommand()
        delete_command.execute(self.domain_appointment_1)

        # run checks
        # one object is inserted
        self.assertEqual(Appointment.objects.count(), 1)