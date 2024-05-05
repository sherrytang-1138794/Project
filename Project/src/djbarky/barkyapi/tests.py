from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework import routers
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from .models import Patient, PatientHistory, Appointment
from .views import PatientViewSet, PatientHistoryViewSet, AppointmentViewSet

from django.contrib.auth.models import User #new
# Create your tests here.
# test plan


class PatientTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.patient = Patient.objects.create(
            id=1,
            patient="Emma Stanley",
            age=33,
            phone="8063942045",
            address="4th Ave, Canyon City, TX79015"
        )
        # print(f"patient id: {self.patient.id}")

        # the simple router provides the name 'patient-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:patient-list")
        self.detail_url = reverse(
            "barkyapi:patient-detail", kwargs={"pk": self.patient.id}
        )

    # 1. create a patient
    def test_create_patient(self):
        """
        Ensure we can create a new patient object.
        """

        # the full record is required for the POST
        data = {
            "id": 99,
            "patient": "Marry Greenway",
            "age": 45,
            "phone": "1029382304",
            "address": "1825 Texas Tech Pkwy"
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Patient.objects.count(), 2)
        self.assertEqual(Patient.objects.get(id=99).patient, "Marry Greenway")

    # 2. list patients
    def test_list_patients(self):
        """
        Ensure we can list all patient objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["patient"], self.patient.patient)

    # 3. retrieve a patient
    def test_retrieve_patient(self):
        """
        Ensure we can retrieve a patient object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["patient"], self.patient.patient)

    # 4. delete a patient
    def test_delete_patient(self):
        """
        Ensure we can delete a patient object.
        """
        response = self.client.delete(
            reverse("barkyapi:patient-detail", kwargs={"pk": self.patient.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Patient.objects.count(), 0)

    # 5. update a patient
    def test_update_patient(self):
        """
        Ensure we can update a patient object.
        """
        # the full record is required for the POST
        data = {
            "id": 99,
            "patient": "Marry Greenway",
            "age": 45,
            "phone": "1029382304",
            "address": "1825 Texas Tech Pkwy"
        }
        response = self.client.put(
            reverse("barkyapi:patient-detail", kwargs={"pk": self.patient.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["patient"], "Marry Greenway")



class PatientHistoryTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.patienthistory = PatientHistory.objects.create(
            history_number=1,
            admit_date="2024-05-03",
            symptons="headache, fever",
            department="EMC",
            release_date="2024-05-03",
            patient_id="1",
        )
        # print(f"history number: {self.patienthistory.history_number}")

        # the simple router provides the name 'patienthistory-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:patienthistory-list")
        self.detail_url = reverse(
            "barkyapi:patienthistory-detail", kwargs={"pk": self.patienthistory.history_number}
        )

    # 1. create a patient record
    def test_create_patient_record(self):
        """
        Ensure we can create a new patient history object.
        """
      

        # the full record is required for the POST
        data = {
            "history_number": 99,
            "admit_date": "2024-05-04",
            "symptons": "right hand burnt",
            "department": "EMC",
            "release_date": "2024-05-05",
            "patient_id": "5",
        }
        print(f"data {data}")
        response = self.client.post(self.list_url, data, format="json")
        print(response.data)
        
        print(f"testing history number: {self.patienthistory.history_number}")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(PatientHistory.objects.count(), 2)
        self.assertEqual(PatientHistory.objects.get(history_number=99).symptons, "right hand burnt")

    # 2. list patient records
    def test_list_patient_records(self):
        """
        Ensure we can list all patient history objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["symptons"], self.patienthistory.symptons)

    # 3. retrieve a patient record
    def test_retrieve_patient_record(self):
        """
        Ensure we can retrieve a patient history object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["patient_id"], self.patienthistory.patient_id)

    # 4. delete a patient record
    def test_delete_patient_record(self):
        """
        Ensure we can delete a patient history object.
        """
        response = self.client.delete(
            reverse("barkyapi:patienthistory-detail", kwargs={"pk": self.patienthistory.history_number})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Patient.objects.count(), 0)

    # 5. update a patient record
    def test_update_patient_record(self):
        """
        Ensure we can update a patient history object.
        """
        # the full record is required for the POST
        data = {
            "history_number": 99,
            "admit_date": "2024-05-04",
            "symptons": "right hand burnt",
            "department": "EMC",
            "release_date": "2024-05-05",
            "patient_id": "5"
        }
        response = self.client.put(
            reverse("barkyapi:patienthistory-detail", kwargs={"pk": self.patienthistory.history_number}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["symptons"], "right hand burnt")


class AppointmentTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.appointment = Appointment.objects.create(
            id=1,
            appointment_date="2024-05-02",
            appointment_time="18:30:00",
            status=False,
            patient= "Emily White",
            doctor="WS"
        )
        # print(f"patient name: {self.appointment.patient}")

        # the simple router provides the name 'patient-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:appointment-list")
        self.detail_url = reverse(
            "barkyapi:appointment-detail", kwargs={"pk": self.appointment.id}
        )

    # 1. create an appointment
    def test_create_appointment(self):
        """
        Ensure we can create a new appointment object.
        """

        # the full record is required for the POST
        data = {
            "id": 99,
            "appointment_date": "2024-05-05",
            "appointment_time": "12:30:00",
            "status": False,
            "patient": "Henry Brown",
            "doctor": "HT"
        }
        response = self.client.post(self.list_url, data, format="json")
        print(response.data)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Appointment.objects.count(), 2)
        self.assertEqual(Appointment.objects.get(id=99).patient, "Henry Brown")

    # 2. list appointments
    def test_list_appointments(self):
        """
        Ensure we can list all appointment objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["patient"], self.appointment.patient)

    # 3. retrieve an appointment
    def test_retrieve_appointment(self):
        """
        Ensure we can retrieve an appointment object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["patient"], self.appointment.patient)

    # 4. delete an appointment
    def test_delete_appointment(self):
        """
        Ensure we can delete an appointment object.
        """
        response = self.client.delete(
            reverse("barkyapi:appointment-detail", kwargs={"pk": self.appointment.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)

    # 5. update an appointment
    def test_update_patient(self):
        """
        Ensure we can update an appointment object.
        """
        # the full record is required for the POST
        data = {
            "id": 1,
            "appointment_date": "2024-05-05",
            "appointment_time": "12:30:00",
            "status": False,
            "patient": "Henry Brown",
            "doctor": "HT"
        }
        response = self.client.put(
            reverse("barkyapi:appointment-detail", kwargs={"pk": self.appointment.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["patient"], "Henry Brown")
