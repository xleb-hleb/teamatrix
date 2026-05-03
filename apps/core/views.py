from django.views.generic import ListView, DetailView

from .models import News, TeamMember


class IndexView(ListView):
    model = News
    template_name = "core/index.html"
    context_object_name = "news_list"
    queryset = News.objects.filter(is_published=True)[:6]


class NewsDetailView(DetailView):
    model = News
    template_name = "core/news_detail.html"
    context_object_name = "news"
    queryset = News.objects.filter(is_published=True)


class TeamView(ListView):
    model = TeamMember
    template_name = "core/team.html"
    context_object_name = "team_members"
