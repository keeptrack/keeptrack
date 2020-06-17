import calendar
from datetime import datetime, timedelta, date

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.views import generic

from hire.models import HireRequest, Event
from .forms import HireForm, EventForm
from .utils import Calendar


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


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
        delete = format_html(f'<tr><td colspan="2"><input type="submit" name="delete" value="Delete" class="btn '
                             f'btn-info right"></td></tr> ')
    else:
        instance = HireRequest()
        delete = None

    if request.POST:
        if 'id' in request.POST and request.POST['id'] != 'None':
            hire_id = request.POST['id']
            instance = get_object_or_404(HireRequest, pk=hire_id)

    is_delete = False

    if 'delete' in request.POST:
        post = request.POST.copy()
        post['is_hidden'] = True
        request.POST = post
        is_delete = True

    form = HireForm(request.POST or None, instance=instance)
    if request.POST and (form.is_valid() or is_delete):
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/hire.html', {'form': form, 'delete': delete, 'id': hire_id})


def event(request, event_id=None):
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
        delete = format_html('<tr><td colspan="2"><input type="submit" name="delete" value="Delete" class="btn '
                             'btn-info right"></td></tr>')
    else:
        instance = Event()
        delete = None

    if request.POST:
        if 'id' in request.POST and request.POST['id'] != 'None':
            event_id = request.POST['id']
            instance = get_object_or_404(Event, pk=event_id)

    is_delete = False

    if request.POST and 'delete' in request.POST:
        post = request.POST.copy()
        post['is_hidden'] = True
        request.POST = post
        is_delete = True

    form = EventForm(request.POST or None, instance=instance)

    if request.POST and (form.is_valid() or is_delete):
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form, 'delete': delete, 'id': event_id})
