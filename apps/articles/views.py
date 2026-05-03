from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.urls import reverse
from django.views.generic import DetailView, ListView

from apps.blog.models import Thread
from .models import Article, Category


class ArticleListView(ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"
    paginate_by = 12

    def get_queryset(self):
        qs = Article.objects.filter(is_published=True).select_related("category")
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            self.current_category = Category.objects.filter(slug=category_slug).first()
            if self.current_category:
                qs = qs.filter(category=self.current_category)
        else:
            self.current_category = None
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["current_category"] = getattr(self, "current_category", None)

        breadcrumbs = [{"name": "Каталог статей", "url": reverse("articles:article_list")}]
        if self.current_category:
            for cat in self.current_category.get_breadcrumbs():
                breadcrumbs.append({
                    "name": cat.name,
                    "url": reverse("articles:category_articles", args=[cat.slug]),
                })
        context["breadcrumbs"] = breadcrumbs
        return context


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    context_object_name = "article"
    queryset = Article.objects.filter(is_published=True).select_related("category")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Article.objects.filter(pk=obj.pk).update(views_count=F("views_count") + 1)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        breadcrumbs = [{"name": "Каталог статей", "url": reverse("articles:article_list")}]
        for cat in article.category.get_breadcrumbs():
            breadcrumbs.append({
                "name": cat.name,
                "url": reverse("articles:category_articles", args=[cat.slug]),
            })
        breadcrumbs.append({"name": article.title, "url": ""})
        context["breadcrumbs"] = breadcrumbs
        context["forum_threads"] = (
            Thread.objects.filter(article=article)
            .select_related("author")
            .order_by("-updated_at")[:5]
        )
        context["forum_thread_count"] = Thread.objects.filter(article=article).count()
        return context
