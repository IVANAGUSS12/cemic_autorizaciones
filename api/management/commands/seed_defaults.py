from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Sector, Specialty, Doctor
import os

class Command(BaseCommand):
    help = "Seed default sectors, specialties, doctors, and optional admin user"

    def handle(self, *args, **kwargs):
        # Sectors
        Sector.objects.get_or_create(code="trauma", defaults={"name":"Traumatología"})
        Sector.objects.get_or_create(code="hemo", defaults={"name":"Hemodinamia"})

        # Basic specialties (extend with your Reporte.xls later if desired)
        for name in ["Traumatología","Hemodinamia","Cardiología","Clínica Médica","Diagnóstico por Imágenes"]:
            from django.utils.text import slugify
            Specialty.objects.get_or_create(name=name, defaults={"slug": slugify(name)})

        # Optional admin
        User = get_user_model()
        admin_user = os.getenv("DJANGO_ADMIN_USER","admin")
        admin_pass = os.getenv("DJANGO_ADMIN_PASS","admin123")
        admin_email = os.getenv("DJANGO_ADMIN_EMAIL","admin@example.com")
        if not User.objects.filter(username=admin_user).exists():
            User.objects.create_superuser(username=admin_user, email=admin_email, password=admin_pass)
            self.stdout.write(self.style.SUCCESS(f"Superusuario creado: {admin_user}/{admin_pass}"))
        else:
            self.stdout.write("Superusuario existente")
        self.stdout.write(self.style.SUCCESS("Seed OK"))
