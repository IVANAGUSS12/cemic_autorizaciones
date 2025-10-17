from django.contrib import admin
from .models import Sector, Specialty, Doctor, Patient, Attachment

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("code","name")

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("name","slug")
    prepopulated_fields = {"slug":("name",)}

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name","specialty")
    search_fields = ("name",)

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id","nombre","dni","cobertura","medico","sector","fecha_cx","estado","created_at")
    list_filter = ("estado","sector","fecha_cx","created_at")
    search_fields = ("nombre","dni","cobertura","medico")
    inlines = [AttachmentInline]

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id","patient","kind","file","external_url","uploaded_at")
    list_filter = ("kind","uploaded_at")
