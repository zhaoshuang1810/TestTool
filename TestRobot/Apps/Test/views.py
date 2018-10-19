from django.shortcuts import render

# Create your views here.

from Config.project import projectName

param_dict = {"project":projectName}

def index(request):
    param_dict['title'] = '首页'
    return render(request, 'index.html', param_dict)