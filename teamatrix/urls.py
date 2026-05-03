from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Teamatrix - админ панель"
admin.site.site_title = "Teamatrix"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("", include("apps.core.urls")),
    path("articles/", include("apps.articles.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("humanoid/", include("apps.humanoids.urls")),
    path("development/", include("apps.development.urls")),
    path("events/", include("apps.events.urls")),
    path("equipment/", include("apps.equipment.urls")),
    path("forum/", include("apps.blog.urls")),
    path("ulstu/", include("apps.ulstu.urls")),
    path("cloud/", include("apps.cloud.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
