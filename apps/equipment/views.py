from django.views.generic import ListView, TemplateView

from .models import EquipmentCategory, Supplier


class EquipmentIndexView(TemplateView):
    template_name = "equipment/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = EquipmentCategory.objects.prefetch_related("materials").all()
        ctx["suppliers"] = Supplier.objects.prefetch_related("categories").all()
        ctx["selected_category"] = self.request.GET.get("category", "")
        return ctx


class SupplierListView(ListView):
    model = Supplier
    template_name = "equipment/suppliers.html"
    context_object_name = "suppliers"

    def get_queryset(self):
        qs = Supplier.objects.prefetch_related("categories").all()
        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(categories__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = EquipmentCategory.objects.all()
        ctx["selected_category"] = self.request.GET.get("category", "")
        return ctx
