from django.views import generic, View
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404

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
        item = get_object_or_404(HireRequest, pk=kwargs['pk'])
        return render(request, self.template_name, {'hire': item})

    def update(self, request, *args, **kwargs):
        return HttpResponse(f"Request {kwargs['pk']} was updated")
