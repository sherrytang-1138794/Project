from datetime import date



class DomainPatient:
    """
    Patient domain model.
    """

    def __init__(self, id, patient, age, phone, address):
        self.id = id
        self.patient = patient
        self.age = age
        self.phone = phone
        self.address = address

    def get_name(self):
        return f"{self.patient}"
    
    def get_id(self):
        return self.id

    def __str__(self):
        return f"{self.patient}"

class DomainPatientHistory:
    """
    Patient History domain model.
    """

    def __init__(self, history_number, admit_date, symptons, department, release_date, patient_id):
        self.history_number = history_number
        self.admit_date = admit_date
        self.symptons = symptons
        self.department = department
        self.release_date = release_date
        self.patient_id = patient_id
        # self.doctor = doctor

    # def get_name(self):
    #     return f"{self.patient.first_name} {self.patient.last_name}"
    
    # def get_id(self):
    #     return self.patient.id

    def __str__(self):
        return f"{self.patient_id} {self.patient_id}"
    

class DomainAppointment:
    """
    Appointment domain model.
    """
    def __init__(self, id, appointment_date, appointment_time, status, patient, doctor):
        self.id = id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status
        self.patient = patient
        # self.patient_id = patient_id
        self.doctor = doctor

    def __str__(self):
        return f"{self.patient} {self.appointment_date} {self.appointment_time}"
        


