import datetime

from django.views.generic import DetailView, ListView

from .models import Event


class EventListView(ListView):
    model = Event
    template_name = "events/index.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = datetime.date.today()
        ctx["upcoming_events"] = Event.objects.filter(is_active=True, date__gte=today).order_by("date")
        ctx["past_events"] = Event.objects.filter(is_active=True, date__lt=today).order_by("-date")[:6]
        ctx["today"] = today
        return ctx


class EventDetailView(DetailView):
    model = Event
    template_name = "events/detail.html"
    context_object_name = "event"
