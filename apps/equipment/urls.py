from django.urls import path

from . import views

app_name = "equipment"

urlpatterns = [
    path("", views.EquipmentIndexView.as_view(), name="index"),
    path("suppliers/", views.SupplierListView.as_view(), name="suppliers"),
]
