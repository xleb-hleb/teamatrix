from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="article_list"),
    path("category/<slug:category_slug>/", views.ArticleListView.as_view(), name="category_articles"),
    path("<slug:slug>/", views.ArticleDetailView.as_view(), name="article_detail"),
]
