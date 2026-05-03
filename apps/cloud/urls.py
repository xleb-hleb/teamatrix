from django.urls import path

from . import views

app_name = "cloud"

urlpatterns = [
    path("download/<int:pk>/", views.cloud_download, name="download"),
]
