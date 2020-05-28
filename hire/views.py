from django.http import HttpResponseRedirect
from django.shortcuts import render
import os


def index(request):
    return render(request, 'hire/index.html', {})


def details(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        hire_from = request.POST.get('hire_from')
        hire_to = request.POST.get('hire_to')
        information = request.POST.get('information', '')
        log(name, email, hire_from, hire_to, information)
    return HttpResponseRedirect("/hire/")


def log(name, email, hire_from, hire_to, information):
    current_dir = os.path.dirname(__file__)
    f = open(os.path.join(current_dir, "skeleton_log.txt"), "w")
    f.write(name + "\n")
    f.write(email + "\n")
    f.write(hire_from + "\n")
    f.write(hire_to + "\n")
    f.write(information + "\n")
    f.close()
