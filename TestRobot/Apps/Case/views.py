import json
import os

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Business.models import Business
from Case.method import createcase, getdata, insertbusiness, run_robot_cmd, run_case_cmd
from Case.models import CaseBdd, CaseBddToBusiness, SuiteName
from Config.directory import bus_dir, case_dir
from Config.project import projectName
from Tag.models import Case, Function

param_dict = {"project": projectName}


def index(request):
    param_dict['title'] = '首页'
    return render(request, 'index.html', param_dict)


def bdd(request):
    param_dict['title'] = '行为驱动测试用例'
    casetags_list = [(c.id, c.tag, c.tagName) for c in Case.objects.all()]
    funtags_list = [(f.id, f.tag, f.tagName) for f in Function.objects.all()]
    funtags_list.insert(0, (0, "all", "全部"))
    tags_list = {'casetags': casetags_list,
                 'funtags': funtags_list
                 }
    param_dict.update(tags_list)
    casetag = request.GET.get('casetag', 'InterfaceTest')
    funtag = request.GET.get('funtag', 'all')

    param_dict['selectcasetag'] = casetag
    param_dict['selectfuntag'] = funtag
    param_dict['data'] = getdata(casetag=casetag, funtag=funtag)
    return render(request, 'test/bdd.html', param_dict)


def createsuitebdd(request):
    casetag = request.GET.get('selectcasetag', 'InterfaceTest')
    suite_nums = request.GET.get('suiteids')
    if suite_nums:
        suite_ids = suite_nums.split(",")
        for suite_id in suite_ids:
            createcase(casetag, suite_id)

    resp = {"success": True}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def runsuitebdd(request):
    casetag = request.GET.get('selectcasetag', 'InterfaceTest')
    tags = [casetag]
    suite_nums = request.GET.get('suiteids')
    if suite_nums:
        suite_ids = suite_nums.split(",")
        for suite_id in suite_ids:
            suitename = SuiteName.objects.get(id=suite_id).suitename
            tags.append(suitename.split('.')[0])
    run_robot_cmd(str(request.user), tags)
    resp = {"success": True}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def createbusiness(request):
    data = []
    casetag = request.GET.get('selectcasetag', 'InterfaceTest')
    bustag = Case.objects.get(tag=casetag).bus.tag
    suite_nums = request.GET.get('suiteids')
    if suite_nums:
        suite_ids = suite_nums.split(",")
        for suite_id in suite_ids:
            caseids = [c['id'] for c in CaseBdd.objects.filter(suite_id=suite_id).all().values('id')]
            funtag = SuiteName.objects.get(id=suite_id).function.tag
            for caseid in caseids:
                busids = [c['bus_id'] for c in
                          CaseBddToBusiness.objects.filter(case_id=caseid).all().values('bus_id')]
            busids = list(set(busids))
            file_dir = os.path.join(bus_dir, bustag, funtag + ".robot")
            for busid in busids:
                if bustag in [b.tag for b in Business.objects.get(id=busid).complete.all()]:
                    data.append(insertbusiness(file_dir, bustag, busid))
                else:
                    data.append("业务--" + Business.objects.get(id=busid).chinesename + "，没有勾选" + bustag + "标签，请勾选！")
    else:
        data.append('未勾选组件！')

    resp = {"success": True, 'complete': True if data else False, 'data': "\n".join(data)}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def sort(request):
    id = request.GET.get('id')
    sort = request.GET.get('sort')
    CaseBdd.objects.filter(id=id).update(sort=sort)
    resp = {"success": True}
    return HttpResponse(json.dumps(resp), content_type="application/json")

def runsinglecase(request):
    casetag = request.GET.get('selectcasetag', 'InterfaceTest')
    id = request.GET.get('id')
    name = request.GET.get('name')

    suitid = CaseBdd.objects.get(id=id).suite.id
    suitname = SuiteName.objects.get(id=suitid).suitename
    funtag = SuiteName.objects.get(id=suitid).function.tag
    file_dir = os.path.join(case_dir,casetag,funtag,suitname)
    run_case_cmd(str(request.user),file_dir,name)

    resp = {"success": True}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def ddd(request):
    param_dict['title'] = '数据驱动测试用例'
    return render(request, 'test/ddd.html', param_dict)
