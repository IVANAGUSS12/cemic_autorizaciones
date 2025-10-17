from django.db import models

class Sector(models.Model):
    code = models.SlugField(max_length=20, unique=True)  # 'trauma', 'hemo'
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class Specialty(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=120)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = [("name","specialty")]

    def __str__(self):
        return self.name

class Patient(models.Model):
    ESTADOS = [
        ("Pendiente","Pendiente"),
        ("Solicitado","Solicitado"),
        ("Rechazado por cobertura","Rechazado por cobertura"),
        ("Autorizado","Autorizado"),
        ("Autorizado material pendiente","Autorizado material pendiente"),
    ]

    nombre = models.CharField(max_length=160)
    dni = models.CharField(max_length=32, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    telefono = models.CharField(max_length=64, blank=True, default="")
    cobertura = models.CharField(max_length=120, blank=True, default="")
    medico = models.CharField(max_length=160, blank=True, default="")  # keep as text for easy input
    observaciones = models.TextField(blank=True, default="")

    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_cx = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=48, choices=ESTADOS, default="Pendiente")

    created_at = models.DateTimeField(auto_now_add=True)

    bucket_path = models.CharField(max_length=300, blank=True, default="")  # optional link
    folder_url = models.URLField(blank=True, default="")

    def __str__(self):
        return f"{self.nombre} ({self.dni})"

class Attachment(models.Model):
    KINDS = [
        ("orden","orden"),
        ("dni","dni"),
        ("credencial","credencial"),
        ("materiales","materiales"),
        ("otro","otro"),
    ]
    patient = models.ForeignKey(Patient, related_name="attachments", on_delete=models.CASCADE)
    kind = models.CharField(max_length=24, choices=KINDS, default="otro")
    file = models.FileField(upload_to="attachments/", blank=True, null=True)
    external_url = models.URLField(blank=True, default="")
    name = models.CharField(max_length=140, blank=True, default="")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kind} - {self.patient_id}"
