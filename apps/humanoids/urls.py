from django.urls import path

from . import views

app_name = "humanoids"

urlpatterns = [
    path("", views.HumanoidIndexView.as_view(), name="index"),
    path("articles/", views.HumanoidPostListView.as_view(), name="post_list"),
    path("articles/<slug:slug>/", views.HumanoidPostDetailView.as_view(), name="post_detail"),
    path("videos/", views.HumanoidVideoListView.as_view(), name="video_list"),
]
