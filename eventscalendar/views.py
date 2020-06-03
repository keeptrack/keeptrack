# Create your views here.
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import ListView

from .models import Event
from .utils import Calendar


class CalendarView(ListView):
    model = Event
    template_name = 'calendar.html'


success_url = reverse_lazy("calendar")


def get_context_data(self):
    context = super().get_queryset()

    d = self.request.GET.get('month', None)

    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(d.year, d.month, withyear=True)

    context['calendar'] = mark_safe(html_cal)
    context['prev_month'] = prev_month(d)
    context['next_month'] = next_month(d)

    return context


def prev_month(d):
    return d.month - 1


def next_month(d):
    return d.month - 1
