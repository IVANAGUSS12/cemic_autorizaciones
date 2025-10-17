# CEMIC Autorizaciones · Django + DRF + Panel + QR

Incluye:
- API REST `/v1/patients/`, `/v1/attachments/`, `/v1/sectors/`
- Autenticación por sesión (login/password de Django)
- Admin `/admin/` + cambio de contraseña `/accounts/password_change/`
- Panel interno listo para usar (usa `/v1/patients` y `/v1/attachments`)
- Formulario público (QR) para que el paciente cargue datos y adjuntos
- Dockerfile + docker-compose
- Semillas (`seed_defaults`) para crear sectores y superusuario

## Desarrollo local (Docker)

```bash
cd backend
docker compose up --build
# abrir http://localhost:8080/admin
# panel: http://localhost:8080/static/qr/index.html (form público)
```

## Deploy en DigitalOcean App Platform (Dockerfile)

1. Subí este repo a GitHub.
2. En DO App Platform, crea una App desde el repo y seleccioná el directorio `backend`.
3. Variables de entorno (Build & Run):
   - `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`
   - `DJANGO_SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=*`, `CORS_ALLOW_ALL=True`
4. Activa persistencia si querés almacenar `/app/media` o usa Spaces/S3 (no requerido para prueba).
5. DO ejecutará `Dockerfile` → `entrypoint.sh` aplica migraciones, collectstatic y seed.

## Endpoints principales

- `GET/POST /v1/patients/`
- `GET/PATCH /v1/patients/<id>/`
- `POST /v1/attachments/` (multipart: `patient`, `kind`, `file`)
- `GET /accounts/login/` (login)
- `GET /accounts/logout/`
- `GET /accounts/password_change/`

## Panel y QR

- Panel interno (tu HTML): `backend/templates/index-panel.html` está integrado a la API.
- Form QR público: `backend/templates/qr/index.html`
- Gracias: `backend/templates/qr/gracias.html`

> Nota: El formulario público POSTea a `/v1/patients/` y luego sube archivos a `/v1/attachments/`.
> Si ubicás el sitio detrás de un subpath, ajustá `BASE` en `qr/index.html`.

## Especialidades y paneles por especialidad

- Este backend modela `Specialty` y `Doctor`. Podés crear **vistas/paneles por especialidad** filtrando por `medico` o agregando un campo `specialty` a los pacientes si lo necesitás.
- El panel actual permite filtrar por coberturas, médicos, estado, sector y fechas. Para un “panel por especialidad” duplicá el HTML y dejalo precargado con un filtro de médico/especialidad o crea rutas nuevas que llamen a la misma API con `?medico=` o `?sector__code=`.

## Cargar lista de médicos y especialidades

- Desde `admin/` creá `Specialty` y `Doctor`.
- Si tenés un Excel `Reporte.xls`, podés migrarlo con un comando custom (ver `api/management/commands/import_reporte.py`, opcional).



## URLs por especialidad
- General: `/panel/` → redirige a `index-panel.html` (tu panel general)
- Por especialidad: `/panel/<slug>/` → redirige a `index-panel.html?specialty=<slug>`
  - Ejemplo: `/panel/cardiologia`

Tu panel puede leer `?specialty=slug` para filtrar automáticamente.

## Cargar Especialidades y Médicos desde Excel
Ubicá tu `Reporte.xls` en el servidor (o monta un volumen) y ejecutá:

```bash
python manage.py import_reporte --path /ruta/Reporte.xls
# Si fuese necesario especificar columnas:
python manage.py import_reporte --path /ruta/Reporte.xls --col-especialidad "Especialidad" --col-medico "Medico"
```

## Campos dinámicos en QR
Se incluye `/static/qr/dynamic.js`, que:
- Completa el `<select>` de **Especialidad** con `/v1/specialties/`.
- Completa el `<select>` de **Médico** según la especialidad (`/v1/doctors/?specialty_slug=...`).

> El script detecta automáticamente selects por id/name comunes (`especialidad`, `medico`). Si tus ids o names son distintos, podés ajustarlos en `static/qr/dynamic.js`.
