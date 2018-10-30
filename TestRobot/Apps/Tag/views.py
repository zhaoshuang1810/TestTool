import json
import os

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from Case.models import SuiteName
from Config.directory import case_dir, bus_dir
from Config.project import projectName
from Tag.models import Case, Function, Business

param_dict = {"project": projectName}


def generator(request):
    param_dict['title'] = '代码生成器'
    if str(request.user) == "admin":
        return render(request, 'generator.html', param_dict)
    else:
        return HttpResponseRedirect("/")


def initdir(request):
    casetags = [c['tag'] for c in Case.objects.all().values('tag')]
    casetags.remove('InterfaceDocument')
    funtags = [f['tag'] for f in Function.objects.all().values('tag')]

    for tag in casetags:
        if not os.path.exists(os.path.join(case_dir, tag)):
            os.makedirs(os.path.join(case_dir, tag))
        for tag2 in funtags:
            if not os.path.exists(os.path.join(case_dir, tag, tag2)):
                os.makedirs(os.path.join(case_dir, tag, tag2))

    suitenames = [s['suitename'] for s in SuiteName.objects.all().values('suitename')]
    for suite in suitenames:
        funtag = SuiteName.objects.get(suitename=suite).function.tag
        for tag in casetags:
            if not os.path.exists(os.path.join(case_dir, tag, funtag, suite)):
                open(os.path.join(case_dir, tag, funtag, suite), 'w')

    bustags =  [b['tag'] for b in Business.objects.all().values('tag')]
    for tag in bustags:
        if not os.path.exists(os.path.join(bus_dir, tag)):
            os.makedirs(os.path.join(bus_dir, tag))

    resp = {"success": True}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def initbusiness(request):
    fun = [(f['tag'], f['tagName']) for f in Function.objects.all().values( 'tag', 'tagName')]
    bustags = [b['tag'] for b in Business.objects.all().values('tag')]
    for bustag in bustags:
        for funtag, funtagname in fun:
            file_dir = os.path.join(bus_dir, bustag, funtag + ".robot")
            if not os.path.exists(file_dir):
                content = []
                content.append("*** Settings ***\n")
                content.append("Documentation        " + funtagname + "\n")
                content.append("Library              Collections\n")
                content.append("Library              ../../Library/SqlDjango.py\n")
                if bustag == 'Request':
                    content.append("Library              ../../Library/LibRequest.py\n")
                elif bustag == "Appium":
                    content.append("Library              AppiumLibrary\n")
                elif bustag == 'Selenium':
                    content.append('Library              SeleniumLibrary\n')
                else:
                    pass

                content.append('\n\n')
                content.append('*** Keywords ***\n')
                with open(file_dir, "w", encoding='utf-8') as f:
                    f.writelines(content)

    resp = {"success": True}
    return HttpResponse(json.dumps(resp), content_type="application/json")