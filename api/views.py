from rest_framework import viewsets, permissions, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Patient, Attachment, Sector, Specialty, Doctor
from .serializers import PatientSerializer, PatientDetailSerializer, AttachmentSerializer, SectorSerializer, SpecialtySerializer, DoctorSerializer

class IsStaffOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    permission_classes = [IsStaffOrAuthenticated]
    serializer_class = PatientSerializer

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return PatientDetailSerializer
        return PatientSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params
        cobertura = q.get("cobertura") or ""
        estado = q.get("estado") or ""
        medico = q.get("medico") or ""
        sector = q.get("sector") or q.get("sector__code") or ""
        search = q.get("search") or q.get("q") or ""

        if cobertura: qs = qs.filter(cobertura=cobertura)
        if estado: qs = qs.filter(estado=estado)
        if medico: qs = qs.filter(medico=medico)
        if sector:
            qs = qs.filter(sector__code=sector) if not sector.isdigit() else qs.filter(sector_id=int(sector))
        if search:
            s = search.strip()
            qs = qs.filter(Q(nombre__icontains=s)|Q(dni__icontains=s)|Q(cobertura__icontains=s))
        return qs

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all().order_by("-uploaded_at")
    permission_classes = [IsStaffOrAuthenticated]
    serializer_class = AttachmentSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    permission_classes = [IsStaffOrAuthenticated]
    serializer_class = SectorSerializer


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialty.objects.all().order_by("name")
    permission_classes = [permissions.AllowAny]  # público para QR
    serializer_class = SpecialtySerializer

class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.select_related("specialty").all().order_by("name")
    permission_classes = [permissions.AllowAny]  # público para QR
    serializer_class = DoctorSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        spec = self.request.query_params.get("specialty") or self.request.query_params.get("specialty_id") or ""
        slug = self.request.query_params.get("specialty_slug") or ""
        if spec.isdigit():
            qs = qs.filter(specialty_id=int(spec))
        elif slug:
            qs = qs.filter(specialty__slug=slug)
        return qs
