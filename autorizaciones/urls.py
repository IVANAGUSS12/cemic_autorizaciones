from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import re_path

def panel_root(request):
    return HttpResponseRedirect("/static/index-panel.html")

def panel_by_slug(request, slug):
    # Redirige al panel con query de especialidad para que el JS del panel lo use
    return HttpResponseRedirect(f"/static/index-panel.html?specialty={slug}")


urlpatterns = [
    path("panel/", panel_root, name="panel-root"),
    path("panel/<slug:slug>/", panel_by_slug, name="panel-by-slug"),

    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout/password
    path("v1/", include("api.urls")),
    # Serve the QR public form and thanks from static
    re_path(r"^static/qr/index\.html$", TemplateView.as_view(template_name="qr/index.html"), name="qr-index"),
    re_path(r"^static/qr/gracias\.html$", TemplateView.as_view(template_name="qr/gracias.html"), name="qr-gracias"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
