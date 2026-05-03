from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from .models import Application, PrivacyPolicy, RoadmapStage, UlstuTeam


class UlstuIndexView(TemplateView):
    template_name = "ulstu/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["roadmap"] = RoadmapStage.objects.all()
        ctx["teams"] = UlstuTeam.objects.prefetch_related("members").all()
        return ctx


class PrivacyPolicyView(TemplateView):
    template_name = "ulstu/privacy_policy.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["policy"] = PrivacyPolicy.objects.order_by("-updated_at").first()
        return ctx


class ApplicationSubmitView(View):
    def post(self, request):
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        specialty = request.POST.get("specialty", "").strip()
        motivation = request.POST.get("motivation", "").strip()
        consent = request.POST.get("consent_personal_data")

        if not (name and email and specialty and motivation):
            messages.error(request, "Пожалуйста, заполните все обязательные поля.")
            return redirect("ulstu:index")

        if not consent:
            messages.error(request, "Необходимо дать согласие на обработку персональных данных.")
            return redirect("ulstu:index")

        Application.objects.create(
            name=name,
            email=email,
            phone=phone,
            specialty=specialty,
            motivation=motivation,
        )
        messages.success(request, "Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.")
        return redirect("ulstu:index")
