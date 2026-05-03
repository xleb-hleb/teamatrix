from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView

from apps.articles.models import Article
from .models import Post, Thread


class ForumListView(ListView):
    model = Thread
    template_name = "blog/forum_list.html"
    context_object_name = "threads"
    paginate_by = 20

    def get_queryset(self):
        qs = (
            Thread.objects.select_related("author", "article")
            .annotate(post_count=Count("posts", filter=Q(posts__is_deleted=False)))
        )
        filter_type = self.request.GET.get("type", "")
        article_id = self.request.GET.get("article", "")
        if filter_type == "articles":
            qs = qs.filter(article__isnull=False)
        elif article_id:
            qs = qs.filter(article_id=article_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_type"] = self.request.GET.get("type", "")
        ctx["article_id"] = self.request.GET.get("article", "")
        ctx["total_count"] = Thread.objects.count()
        ctx["article_threads_count"] = Thread.objects.filter(article__isnull=False).count()
        if ctx["article_id"]:
            ctx["filter_article"] = Article.objects.filter(pk=ctx["article_id"]).first()
        return ctx


class ThreadDetailView(DetailView):
    model = Thread
    template_name = "blog/thread_detail.html"
    context_object_name = "thread"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        Thread.objects.filter(pk=self.object.pk).update(views_count=self.object.views_count + 1)
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["posts"] = (
            self.object.posts.filter(is_deleted=False)
            .select_related("author", "reply_to", "reply_to__author")
        )
        return ctx


class CreateThreadView(LoginRequiredMixin, View):
    def get(self, request):
        article_id = request.GET.get("article")
        article = None
        if article_id:
            article = get_object_or_404(Article, pk=article_id, is_published=True)
        return render(request, "blog/create_thread.html", {"article": article})

    def post(self, request):
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        article_id = request.POST.get("article_id", "").strip()

        if not title or not content:
            messages.error(request, "Заголовок и текст первого сообщения обязательны.")
            article = Article.objects.filter(pk=article_id, is_published=True).first() if article_id else None
            return render(request, "blog/create_thread.html", {
                "article": article, "title": title, "content": content,
            })

        article = None
        if article_id:
            article = Article.objects.filter(pk=article_id, is_published=True).first()

        thread = Thread.objects.create(title=title, author=request.user, article=article)
        Post.objects.create(thread=thread, author=request.user, content=content)
        messages.success(request, "Тема создана.")
        return redirect("blog:thread_detail", pk=thread.pk)


class AddPostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk)
        content = request.POST.get("content", "").strip()
        reply_to_id = request.POST.get("reply_to", "").strip()

        if not content:
            messages.error(request, "Сообщение не может быть пустым.")
            return redirect("blog:thread_detail", pk=pk)

        reply_to = None
        if reply_to_id:
            reply_to = Post.objects.filter(pk=reply_to_id, thread=thread, is_deleted=False).first()

        Post.objects.create(thread=thread, author=request.user, content=content, reply_to=reply_to)
        Thread.objects.filter(pk=thread.pk).update(updated_at=timezone.now())
        return redirect("blog:thread_detail", pk=pk)