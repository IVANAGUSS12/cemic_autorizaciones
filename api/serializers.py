from rest_framework import serializers
from .models import Patient, Attachment, Sector, Specialty, Doctor

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ["id","code","name"]

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["id","patient","kind","file","external_url","name","uploaded_at"]

class PatientSerializer(serializers.ModelSerializer):
    sector__code = serializers.SerializerMethodField()
    class Meta:
        model = Patient
        fields = ["id","nombre","dni","email","telefono","cobertura","medico","observaciones",
                  "sector","sector__code","fecha_cx","estado","created_at","bucket_path","folder_url","attachments"]
        read_only_fields = ["attachments"]
        depth = 0

    def get_sector__code(self, obj):
        return obj.sector.code if obj.sector else ""

class PatientDetailSerializer(PatientSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ["id","name","slug"]

class DoctorSerializer(serializers.ModelSerializer):
    specialty = SpecialtySerializer(read_only=True)
    specialty_id = serializers.PrimaryKeyRelatedField(
        queryset=Specialty.objects.all(), source="specialty", write_only=True, required=False
    )
    class Meta:
        model = Doctor
        fields = ["id","name","specialty","specialty_id"]
