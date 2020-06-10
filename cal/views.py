import calendar
from datetime import datetime, timedelta, date

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic

from hire.models import HireRequest, Event
from .forms import HireForm, EventForm
from .utils import Calendar


class CalendarView(generic.ListView):
    template_name = 'cal/calendar.html'
    context_object_name = 'event_list'
    model = HireRequest

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)
        context['event_list'] = Event.objects
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(d.year, d.month, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    p_month = first - timedelta(days=1)
    month = 'month=' + str(p_month.year) + '-' + str(p_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    n_month = last + timedelta(days=1)
    month = 'month=' + str(n_month.year) + '-' + str(n_month.month)
    return month


def hire(request, hire_id=None):
    if hire_id:
        instance = get_object_or_404(HireRequest, pk=hire_id)
    else:
        instance = HireRequest()

    form = HireForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/hire.html', {'form': form})


def event(request, event_id=None):
    if event_id:
        instance = get_object_or_404(HireRequest, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})

def hire(request, hire_id=None):
    if hire_id:
        instance = get_object_or_404(HireRequest, pk=hire_id)
    else:
        instance = HireRequest()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/hire.html', {'form': form})
