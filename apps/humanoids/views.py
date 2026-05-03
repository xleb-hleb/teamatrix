from django.views.generic import DetailView, ListView, TemplateView

from .models import HumanoidPost, HumanoidVideo


class HumanoidIndexView(TemplateView):
    template_name = "humanoids/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["posts"] = HumanoidPost.objects.filter(is_published=True)[:6]
        ctx["videos"] = HumanoidVideo.objects.filter(is_published=True)[:4]
        return ctx


class HumanoidPostListView(ListView):
    model = HumanoidPost
    template_name = "humanoids/post_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        return HumanoidPost.objects.filter(is_published=True)


class HumanoidPostDetailView(DetailView):
    model = HumanoidPost
    template_name = "humanoids/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return HumanoidPost.objects.filter(is_published=True)


class HumanoidVideoListView(ListView):
    model = HumanoidVideo
    template_name = "humanoids/video_list.html"
    context_object_name = "videos"
    paginate_by = 12

    def get_queryset(self):
        return HumanoidVideo.objects.filter(is_published=True)
