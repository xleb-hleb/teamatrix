from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.ForumListView.as_view(), name="index"),
    path("create/", views.CreateThreadView.as_view(), name="create_thread"),
    path("<int:pk>/", views.ThreadDetailView.as_view(), name="thread_detail"),
    path("<int:pk>/post/", views.AddPostView.as_view(), name="add_post"),
]