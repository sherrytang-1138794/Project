from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"patients", views.PatientViewSet)
router.register(r"patienthistories", views.PatientHistoryViewSet)
router.register(r"appointments", views.AppointmentViewSet)
router.register(r"users", views.UserViewSet)

app_name = "barkyapi"

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include(router.urls)),
]

# add the router's URLs to the urlpatterns
urlpatterns += router.urls


