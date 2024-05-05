from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Patient, PatientHistory, Appointment
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, PatientSerializer, PatientHistorySerializer, AppointmentSerializer


# Create your views here.
class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    """
    queryset = Patient.objects.all().order_by("-id")
    serializer_class = PatientSerializer

class PatientHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patient's history to be viewed or edited.
    """

    queryset = PatientHistory.objects.all().order_by("-admit_date")
    serializer_class = PatientHistorySerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows appointments to be viewed or edited.
    """

    queryset = Appointment.objects.all().order_by("-appointment_date")
    serializer_class = AppointmentSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


# class SnippetViewSet(viewsets.ModelViewSet):
#     """
#     This ViewSet automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.

#     Additionally we also provide an extra `highlight` action.
#     """

#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#     @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
#     def highlight(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
