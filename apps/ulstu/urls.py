from django.urls import path

from . import views

app_name = "ulstu"

urlpatterns = [
    path("", views.UlstuIndexView.as_view(), name="index"),
    path("apply/", views.ApplicationSubmitView.as_view(), name="apply"),
    path("privacy/", views.PrivacyPolicyView.as_view(), name="privacy_policy"),
]
