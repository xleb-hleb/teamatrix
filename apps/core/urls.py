from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("team/", views.TeamView.as_view(), name="team"),
    path("news/<slug:slug>/", views.NewsDetailView.as_view(), name="news_detail"),
]
