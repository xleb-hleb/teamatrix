from django.urls import path

from . import views

app_name = "development"

urlpatterns = [
    path("", views.DevelopmentIndexView.as_view(), name="index"),
    path("subsystem/<slug:slug>/", views.SubsystemDetailView.as_view(), name="subsystem_detail"),
    path("part/<str:key>/", views.RobotBodyPartDetailView.as_view(), name="robot_part_detail"),
    # Admin annotation tool
    path("admin-tools/annotate/",      views.admin_annotate_view, name="admin_annotate"),
    path("admin-tools/annotate/save/", views.admin_annotate_save, name="admin_annotate_save"),
]
