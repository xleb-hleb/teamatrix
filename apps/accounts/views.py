from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView

from apps.articles.models import Article
from apps.core.models import News

from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:dashboard")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Регистрация прошла успешно!")
        return redirect(self.success_url)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context["bookmarked_articles"] = profile.bookmarked_articles.filter(is_published=True)
        context["bookmarked_news"] = profile.bookmarked_news.filter(is_published=True)
        context["subscribed_categories"] = profile.subscribed_categories.all()
        context["latest_news"] = News.objects.filter(is_published=True)[:5]
        return context


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
        return render(request, "accounts/profile_edit.html", {
            "user_form": user_form,
            "profile_form": profile_form,
        })

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль обновлён!")
            return redirect("accounts:dashboard")
        return render(request, "accounts/profile_edit.html", {
            "user_form": user_form,
            "profile_form": profile_form,
        })


@login_required
def bookmark_article(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"}, status=405)
    article = get_object_or_404(Article, pk=pk, is_published=True)
    profile = request.user.profile
    if profile.bookmarked_articles.filter(pk=pk).exists():
        profile.bookmarked_articles.remove(article)
        saved = False
    else:
        profile.bookmarked_articles.add(article)
        saved = True
    return JsonResponse({"saved": saved})


@login_required
def bookmark_news(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"}, status=405)
    news = get_object_or_404(News, pk=pk, is_published=True)
    profile = request.user.profile
    if profile.bookmarked_news.filter(pk=pk).exists():
        profile.bookmarked_news.remove(news)
        saved = False
    else:
        profile.bookmarked_news.add(news)
        saved = True
    return JsonResponse({"saved": saved})
