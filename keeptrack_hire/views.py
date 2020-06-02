from django.views import generic, View
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404

from hire.models import HireRequest

class IndexView(generic.ListView):
    model = HireRequest

class HireView(View):
    template_name = 'keeptrack_hire/edit_hire.html'

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(HireRequest, pk=kwargs['pk'])
        return render(request, self.template_name, {'hire': item})
