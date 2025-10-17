from django.core.management.base import BaseCommand, CommandError
from api.models import Specialty, Doctor
import pandas as pd
from django.utils.text import slugify
import os

class Command(BaseCommand):
    help = "Importa especialidades y médicos desde un Excel (.xls/.xlsx). Columnas esperadas: 'Especialidad', 'Medico' (o similares). Usa --path=/ruta/Reporte.xls"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, required=True, help="Ruta al archivo Excel")

        parser.add_argument("--sheet", type=str, default=None, help="Nombre de hoja (opcional)")

        parser.add_argument("--col-especialidad", type=str, default=None, help="Nombre de columna de especialidad")
        parser.add_argument("--col-medico", type=str, default=None, help="Nombre de columna de médico")

    def handle(self, *args, **opts):
        path = opts["path"]
        sheet = opts["sheet"]
        col_es = opts["col_especialidad"]
        col_md = opts["col_medico"]

        if not os.path.exists(path):
            raise CommandError(f"No existe el archivo: {path}")

        try:
            df = pd.read_excel(path, sheet_name=sheet)  # xlrd 1.2 soporta .xls
        except Exception as e:
            raise CommandError(f"Error leyendo Excel: {e}")

        # Normaliza encabezados
        cols = {str(c).strip().lower(): c for c in df.columns}
        # Heurística si no pasaron nombres
        if not col_es:
            for key in ["especialidad","especialidad/especialista","especialidad_nombre","especialidades"]:
                if key in cols: col_es = cols[key]; break
        if not col_md:
            for key in ["medico","médico","profesional","doctor","dr"]:
                if key in cols: col_md = cols[key]; break

        if not col_es or not col_md:
            raise CommandError(f"No se encontraron columnas. Pasá --col-especialidad y --col-medico. Columnas disponibles: {list(df.columns)}")

        creados_es = creados_md = 0
        for _, row in df[[col_es, col_md]].dropna(how="all").iterrows():
            esp = str(row.get(col_es,"")).strip()
            doc = str(row.get(col_md,"")).strip()
            if not esp and not doc:
                continue
            if esp:
                spec, created = Specialty.objects.get_or_create(name=esp, defaults={"slug": slugify(esp)})
                if created: creados_es += 1
            if doc:
                if esp:
                    spec = Specialty.objects.get(name=esp)
                else:
                    # Si no hay especialidad en la fila, no asociamos
                    spec = None
                from api.models import Doctor
                d = Doctor.objects.filter(name=doc, specialty=spec).first()
                if not d:
                    Doctor.objects.create(name=doc, specialty=spec)
                    creados_md += 1

        self.stdout.write(self.style.SUCCESS(f"Especialidades nuevas: {creados_es} · Médicos nuevos: {creados_md}"))
