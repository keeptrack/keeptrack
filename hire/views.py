from .forms import HireForm
from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    form = HireForm
    return render(request, 'hire/index.html', {'form': form})


def details(request):
    if request.method == 'POST':
        data = {}
        filled_form = HireForm(request.POST)

        if filled_form.is_valid():
            # TODO: Check for duplicates
            hire = filled_form.save()
            filled_form = HireForm()
            data['note'] = f"Thank you {hire.name} for submitting your request. We'll get in touch soon."

        data['form'] = filled_form
        return render(request, 'hire/index.html', data)

    return HttpResponseRedirect("/hire/")
