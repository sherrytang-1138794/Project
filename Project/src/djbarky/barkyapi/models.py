from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

from barkyarch.domain.model import DomainPatient, DomainPatientHistory, DomainAppointment

# pygments stuff
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


# Create your models here.
class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    patient= models.CharField(max_length=255)
    age = models.IntegerField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    # patient_history = models.OneToOneFieldField(PatientHistory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient}"

    class Meta:
        app_label = "barkyapi"

    # these methods are borrowed from P&G
    # it is not clear if they are needed as we are simply translating to and from pure Python
    # objects to Django models and back.
    @staticmethod
    def update_from_domain(domain_patient: DomainPatient):
        try:
            patient = Patient.objects.get(id=domain_patient.id)
        except Patient.DoesNotExist:
            patient = Patient(id=domain_patient.id)

        patient.id = domain_patient.id
        patient.patient = domain_patient.patient
        patient.age = domain_patient.age
        patient.phone = domain_patient.phone
        patient.address = domain_patient.address
        # patient.patient_history = domain_patient.patient_history
        patient.save()

    def to_domain(self) -> DomainPatient:
        p = DomainPatient(
            id=self.id,
            patient=self.patient,
            age=self.age,
            phone=self.phone,
            address=self.address,
            # patient_history=self.patient_history,
        )
        return p

class PatientHistory(models.Model):
    Cardiologist='CL'
    Dermatologists='DL'
    Emergency_Medicine_Specialists='EMC'
    Immunologists='IL'
    Anesthesiologists='AL'
    Colon_and_Rectal_Surgeons='CRS'

    department_choice = [(Cardiologist,'Cardiologist'),
        (Dermatologists,'Dermatologists'),
        (Emergency_Medicine_Specialists,'Emergency Medicine Specialists'),
        (Immunologists,'Immunologists'),
        (Anesthesiologists,'Anesthesiologists'),
        (Colon_and_Rectal_Surgeons,'Colon and Rectal Surgeons')
    ]
    history_number = models.IntegerField(primary_key=True)
    admit_date = models.DateField(verbose_name='Admit Date', auto_now=False, auto_now_add=True)
    symptons = models.CharField(max_length=255)
    department = models.CharField(max_length=5, choices=department_choice, default=Emergency_Medicine_Specialists)
    release_date = models.DateField(verbose_name='Release Date', auto_now=False, auto_now_add=False, null=True, blank=True)
    patient_id = models.CharField(max_length=255)
    # patient = models.ForeignKey("Patient", related_name="patienthistories", on_delete=models.CASCADE)
    # doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient_id} {self.admit_date}"

    class Meta:
        app_label = "barkyapi"

    # these methods are borrowed from P&G
    # it is not clear if they are needed as we are simply translating to and from pure Python
    # objects to Django models and back.
    @staticmethod
    def update_from_domain(domain_patient_history: DomainPatientHistory):
        try:
            patient_history = PatientHistory.objects.get(history_number=domain_patient_history.history_number)
        except PatientHistory.DoesNotExist:
            patient_history = Patient(history_number=domain_patient_history.history_number)
        
        # patient_history.patient_id = domain_patient_history.patient_id
        patient_history.history_number = domain_patient_history.history_number
        patient_history.admit_date = domain_patient_history.admit_date
        patient_history.symptons = domain_patient_history.symptons
        patient_history.department = domain_patient_history.department
        patient_history.release_date = domain_patient_history.release_date
        patient_history.patient_id = domain_patient_history.patient_id
        # patient_history.doctor = domain_patient_history.doctor
        patient_history.save()

    def to_domain(self) -> DomainPatientHistory:
        p = DomainPatientHistory(
            history_number=self.history_number,
            admit_date=self.admit_date,
            symptons=self.symptons,
            department=self.department,
            release_date=self.release_date,
            patient_id=self.patient_id,
            # doctor=self.doctor,
        )
        return p

class Appointment(models.Model):
    Watson='WS'
    Brook='BK'
    Greenway='GW'
    Hiliton='HT'
    

    doctor_choice = [(Watson,'Watson'),
        (Brook,'Brooks'),
        (Greenway,'Greenway'),
        (Hiliton,'Hiliton'),
    ]
    id = models.IntegerField(primary_key=True)
    appointment_date = models.DateField(verbose_name='Appointment date', auto_now=False, auto_now_add=False)
    appointment_time = models.TimeField(verbose_name='Appointment time', auto_now=False, auto_now_add=False)
    status = models.BooleanField(default=False)
    # patient_id = models.CharField(max_length=20)
    # patient= models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient = models.CharField(max_length=255, blank=True)
    doctor = models.CharField(max_length=255, choices=doctor_choice, default=Watson)
    # patient_history = models.OneToOneFieldField(PatientHistory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient}"

    class Meta:
        app_label = "barkyapi"

    # these methods are borrowed from P&G
    # it is not clear if they are needed as we are simply translating to and from pure Python
    # objects to Django models and back.
    @staticmethod
    def update_from_domain(domain_appointment: DomainAppointment):
        try:
            appointment = Appointment.objects.get(patient=domain_appointment.patient)
        except Appointment.DoesNotExist:
            appointment = Appointment(patient=domain_appointment.patient)

        appointment.id = domain_appointment.id
        appointment.appointment_date = domain_appointment.appointment_date
        appointment.appointment_time = domain_appointment.appointment_time
        appointment.status = domain_appointment.status
        appointment.patient = domain_appointment.patient
        # appointment.patient_id = domain_appointment.patient_id
        appointment.doctor = domain_appointment.doctor
        appointment.save()

    def to_domain(self) -> DomainAppointment:
        a = DomainAppointment(
            id=self.id,
            appointment_date=self.appointment_date,
            appointment_time=self.appointment_time,
            status=self.status,
            patient=self.patient,
            # patient_id=self.patient_id,
            doctor=self.doctor,
            
        )
        return a


# class Snippet(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     title = models.CharField(max_length=100, blank=True, default="")
#     code = models.TextField()
#     linenos = models.BooleanField(default=False)
#     language = models.CharField(
#         choices=LANGUAGE_CHOICES, default="python", max_length=100
#     )
#     style = models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)
#     owner = models.ForeignKey(
#         "auth.User", related_name="snippets", on_delete=models.CASCADE
#     )
#     highlighted = models.TextField()

#     class Meta:
#         ordering = ["created"]

#     def save(self, *args, **kwargs):
#         """
#         Use the `pygments` library to create a highlighted HTML
#         representation of the code snippet.
#         """
#         lexer = get_lexer_by_name(self.language)
#         linenos = "table" if self.linenos else False
#         options = {"title": self.title} if self.title else {}
#         formatter = HtmlFormatter(
#             style=self.style, linenos=linenos, full=True, **options
#         )
#         self.highlighted = highlight(self.code, lexer, formatter)
#         super().save(*args, **kwargs)

#     def __str__(self) -> str:
#         return f"{self.title} - {self.id}"
