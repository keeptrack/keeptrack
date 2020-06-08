import datetime
from django.views import generic, View
from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404

from hire.models import HireRequest

def delete_hire(request, **kwargs):
    key = kwargs['pk']
    obj = HireRequest.objects.get(pk=key)
    return HttpResponse(f"Deleting element {key}: {obj}")

class IndexView(generic.ListView):
    model = HireRequest
    ordering = ['-hire_from']

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

class HireView(View):
    template_name = 'keeptrack_hire/edit_hire.html'

    def get(self, request, *args, **kwargs):
        hire = get_object_or_404(HireRequest, pk=kwargs['pk'])
        disabled = 'readonly' if 'edit' not in request.GET else ''
        assets = AllocatedEquipment.objects.filter(request=hire)

        ctx = {
            'hire': hire,
            'disabled': disabled,
            'duration': (hire.hire_to - hire.hire_from).days + 1
        }

        if assets.exists():
            ctx['allocated_assets'] = assets

        return render(request, self.template_name, ctx)

    def _sanitize_soc_string(self, cspId):
        if cspId == '--' or not cspId.isnumeric():
            return ""
        return int(cspId)

    def post(self, request, *args, **kwargs):
        print(request.POST)

        def get_post_or_404(arg):
            if arg not in request.POST:
                raise Http404(f"Did not submit POST parameter {arg}")
            return request.POST.get(arg)

        to_date = lambda str: datetime.datetime.strptime(str, '%Y-%m-%d').date()

        item = get_object_or_404(HireRequest, pk=kwargs['pk'])

        # Override items from request
        item.name = get_post_or_404('hire-name')
        item.email = get_post_or_404('hire-email')
        item.cid = get_post_or_404('hire-cid')
        item.hire_from = to_date(get_post_or_404('hire-from'))
        item.hire_to = to_date(get_post_or_404('hire-to'))

        # TODO: Figure out why DB doesn't update this field.
        item.description = get_post_or_404('hire-desc')

        item.save()

        return HttpResponseRedirect(reverse('keeptrack_hire:edit_hire', kwargs={'pk':item.id}))
