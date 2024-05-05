from .models import Patient, PatientHistory, Appointment, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User
from rest_framework import serializers


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    # history = PatientHistorySerializer()

    class Meta:
        model = Patient
        fields = ("id", "patient", "age", "phone", "address")

class PatientHistorySerializer(serializers.HyperlinkedModelSerializer):
    # patient = PatientSerializer(source='patients', read_only=True)
    # appointment = serializers.PrimaryKeyRelatedField(many=True, queryset=Appointment.objects.all())


    class Meta:
        model = PatientHistory
        fields = ("history_number", "admit_date", "symptons", "department", "release_date", "patient_id")

class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    # patient = serializers.PrimaryKeyRelatedField(many=True, queryset=Patient.objects.all())

    # def get_patient_name(self, obj):
    #     try:
    #         return obj.patient.patient
    #     except ObjectDoesNotExist:
    #         # the day object doesn't have any
    #         # pet associated, so return None
    #         return None
    
    # def create(self, validated_data):
    #     patient = validated_data.pop('patient')
    #     appointment = Appointment.objects.create(patient=patient, **validated_data)
    #     return appointment

    class Meta:
        model = Appointment
        fields = ["id", "appointment_date", "appointment_time", "status", "patient", "doctor"]

# class SnippetSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Snippet
#         owner = serializers.ReadOnlyField(source="owner.username")
#         fields = ["id", "title", "code", "linenos", "language", "style", "owner"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # patient = serializers.PrimaryKeyRelatedField(many=True, queryset=Appointment.objects.all())
        fields = ("id", "username", "password")


