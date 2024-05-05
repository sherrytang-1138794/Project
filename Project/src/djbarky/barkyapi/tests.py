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

    #6. list patients by id
    def test_ordering_by_id_ascending(self):

        url = reverse('barkyapi:patient-list') + '?ordering=id'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['id'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)
    
    def test_ordering_by_id_descending(self):

        url = reverse('barkyapi:patient-list') + '?ordering=-id'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['id'], reverse=True)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    #7. list patients by patient's name
    def test_ordering_by_patient_name_ascending(self):
        url = reverse('barkyapi:patient-list') + '?ordering=patient'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['patient'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)
    
    def test_ordering_by_patient_name_descending(self):
        url = reverse('barkyapi:patient-list') + '?ordering=-patient'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['patient'], reverse=True)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)



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

    # list patient history by patient_id
    def test_ordering_by_patient_id_ascending(self):
        url = reverse('barkyapi:patienthistory-list') + '?ordering=patient_id'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['patient_id'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)
    
    def test_ordering_by_patient_id_descending(self):
        url = reverse('barkyapi:patienthistory-list') + '?ordering=-patient_id'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['patient_id'], reverse=True)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)
    
    # list patient history by admit_date
    def test_ordering_by_admit_date_ascending(self):
        url = reverse('barkyapi:patienthistory-list') + '?ordering=admit_date'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['admit_date'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)
    
    def test_ordering_by_admit_date_descending(self):
        url = reverse('barkyapi:patienthistory-list') + '?ordering=-admit_date'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['admit_date'], reverse=True)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)
    
    # list patient history by department
    def test_ordering_by_department_ascending(self):
        url = reverse('barkyapi:patienthistory-list') + '?ordering=department'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['department'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)
    
    def test_ordering_by_department_descending(self):
        url = reverse('barkyapi:patienthistory-list') + '?ordering=-department'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['department'], reverse=True)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    # test patient history by release_date
    def test_ordering_by_release_date_ascending(self):
        url = reverse('barkyapi:patienthistory-list') + '?ordering=release_date'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['release_date'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)    

    def test_ordering_by_release_date_descending(self):
        url = reverse('barkyapi:patienthistory-list') + '?ordering=-release_date'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['release_date'], reverse=True)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)


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

    # 6. list appointment by appointment_date
    def test_ordering_by_appointment_date_ascending(self):
        url = reverse('barkyapi:appointment-list') + '?ordering=appointment_date'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['appointment_date'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    def test_ordering_by_appointment_descending(self):
        url = reverse('barkyapi:appointment-list') + '?ordering=-appointment_date'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['appointment_date'], reverse=True)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    # list appointment by patient's name
    def test_ordering_by_patient_ascending(self):
        url = reverse('barkyapi:appointment-list') + '?ordering=patient'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['patient'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    def test_ordering_by_patient_descending(self):
        url = reverse('barkyapi:appointment-list') + '?ordering=-patient'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['patient'], reverse=True)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    # list appointment by doctor's name
    def test_ordering_by_doctor_ascending(self):
        url = reverse('barkyapi:appointment-list') + '?ordering=doctor'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['doctor'])
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)

    def test_ordering_by_doctor_descending(self):
        url = reverse('barkyapi:appointment-list') + '?ordering=-doctor'
        response = self.client.get(url)
        response_result = response.json().get('results')
        expected_result = sorted(response_result, key=lambda i: i['doctor'], reverse=True)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response_result, expected_result)   


class UserTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(
            username= "tester", 
            email="tester@mail.com",
            password="Pass12345"
            )
        
        self.client = APIClient() #add
    
        # the simple router provides the name 'user-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:user-list")
        self.detail_url = reverse(
            "barkyapi:user-detail", kwargs={"pk": self.user.id}
        )

    # 11. create a user
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """

        # the full record is required for the POST
        data = {
            "username": "tester_created",
            "email": "tester_c@mail.com",
            "password": "Pass12345"
        }

        response = self.client.post(self.list_url, data, format="json")
        # print("Test Create User")
        # print(response.status_code)
        # print(response.data)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=2).username, "tester_created")

    # 12. retrieve a user
    def test_retrieve_user(self):
        """
        Ensure we can retrieve a user object.
        """
        response = self.client.get(self.detail_url)
        # print(response.data)
        # print(response.status_code)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["username"], self.user.username)

    # 13. delete a user
    def test_delete_user(self):
        """
        Ensure we can delete a user object.
        """
        response = self.client.delete(
            reverse("barkyapi:user-detail", kwargs={"pk": self.user.id})
        )
        # print("Delete User")
        # print(response.data)
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    # 14. list users
    def test_list_users(self):
        """
        Ensure we can list all user objects.
        """
        response = self.client.get(self.list_url)
        # print(response.data)
        # print(response.status_code)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["id"], self.user.id)

    # 15. update a user
    def test_update_user(self):
        """
        Ensure we can update a user object.
        """
        # the full record is required for the POST
        data = {
            "username": "tester",
            "email": "tester@mail.com",
            "password": "Update12345"
        }
            
        response = self.client.put(
            reverse("barkyapi:user-detail", kwargs={"pk": self.user.id}),
            data,
            format="json",
        )
        # print("Update User")
        # print(response.data)
        # print(response.status_code)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["password"], "Update12345")

