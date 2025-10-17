from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PatientViewSet, AttachmentViewSet, SectorViewSet, SpecialtyViewSet, DoctorViewSet

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patients")
router.register(r"attachments", AttachmentViewSet, basename="attachments")
router.register(r"sectors", SectorViewSet, basename="sectors")
router.register(r"specialties", SpecialtyViewSet, basename="specialties")
router.register(r"doctors", DoctorViewSet, basename="doctors")

urlpatterns = [
    path("", include(router.urls)),
]
