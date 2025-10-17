import os
from pathlib import Path
from datetime import timedelta

# --- BASE DIR ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# --- APPS ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    # tus apps:
    "backend",
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- URLS / WSGI ---
ROOT_URLCONF = "autorizaciones.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "autorizaciones.wsgi.application"

# --- DATABASE ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "defaultdb"),
        "USER": os.getenv("DB_USER", "doadmin"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv(
            "DB_HOST", "db-postgresql-sfo3-78425-do-user-27581571-0.b.db.ondigitalocean.com"
        ),
        "PORT": os.getenv("DB_PORT", "25060"),
        "OPTIONS": {
            "sslmode": os.getenv("DB_SSLMODE", "require"),
        },
    }
}

# --- PASSWORDS ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- LANGUAGE / TIME ---
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# --- STATIC & MEDIA ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- DJANGO REST FRAMEWORK ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# --- CORS ---
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL", "True") == "True"

# --- DEFAULT AUTO FIELD ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- SUPERUSER AUTO-CREATION ---
DJANGO_ADMIN_USER = os.getenv("DJANGO_ADMIN_USER", "admin")
DJANGO_ADMIN_PASS = os.getenv("DJANGO_ADMIN_PASS", "admin123")
DJANGO_ADMIN_EMAIL = os.getenv("DJANGO_ADMIN_EMAIL", "admin@example.com")

# Crear superusuario automáticamente si no existe
if os.getenv("CREATE_SUPERUSER", "True") == "True":
    try:
        import django
        django.setup()
        from django.contrib.auth.models import User
        if not User.objects.filter(username=DJANGO_ADMIN_USER).exists():
            User.objects.create_superuser(
                username=DJANGO_ADMIN_USER,
                password=DJANGO_ADMIN_PASS,
                email=DJANGO_ADMIN_EMAIL,
            )
            print("Superusuario creado automáticamente ✅")
    except Exception as e:
        print(f"No se pudo crear superusuario: {e}")

