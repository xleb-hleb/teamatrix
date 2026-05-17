import json

from django.views.generic import ListView, DetailView

from .models import News, RobotLoaderConfig, TeamMember


class IndexView(ListView):
    model = News
    template_name = "core/index.html"
    context_object_name = "news_list"
    queryset = News.objects.filter(is_published=True)[:6]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cfg = RobotLoaderConfig.get_config()
        ctx["eye_cfg_json"] = json.dumps({
            "x":         cfg.eye_x,
            "y":         cfg.eye_y,
            "size":      cfg.eye_size,
            "intensity": cfg.eye_intensity,
            "startT":    cfg.eye_start_t,
        })
        return ctx


class NewsDetailView(DetailView):
    model = News
    template_name = "core/news_detail.html"
    context_object_name = "news"
    queryset = News.objects.filter(is_published=True)


class TeamView(ListView):
    model = TeamMember
    template_name = "core/team.html"
    context_object_name = "team_members"
