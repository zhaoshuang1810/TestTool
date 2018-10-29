import os
import shutil
import time

from Business.models import Business, BusinessToVariable
from Case.models import SuiteName, CaseBdd, CaseBddToBusiness
from Config.directory import case_dir, bus_dir, media_dir
from Data.models import Variable
from Tag.models import Case, Function


def getSetting(casetag, suiteid):
    obj = SuiteName.objects.get(id=suiteid)
    suitename = obj.suitename
    funtag = obj.function.tag
    documentation = obj.documentation
    bustag = Case.objects.get(tag=casetag).bus.tag

    content = []
    content.append("*** Settings ***\n")
    content.append("Documentation     " + documentation + "\n")
    content.append("Force Tags        " + casetag + "    " + funtag + "    " + suitename.split(".")[0] + "\n")

    if bustag == 'Request':
        pass
    else:
        content.append("Suite Setup	         Setup_suite\n")
        content.append("Suite Teardown	     Teardown_suite\n")
        content.append("Test Setup	         Setup_test\n")
        content.append("Test Teardown	     Teardown_test\n")

    content.append("Resource        ../../../Common/" + bustag + ".robot\n")
    bus_name = list(
        filter(None, [y if '.robot' in y else None for y in os.listdir(os.path.join(bus_dir, bustag))]))
    for name in bus_name:
        content.append("Resource        ../../../Business/" + bustag + "/" + name + "\n")

    content.append("\n\n")

    return content


def getCase(suiteid):
    caseids = [c['id'] for c in list(CaseBdd.objects.filter(suite_id=suiteid).order_by('sort').values('id'))]

    content = []
    content.append("*** Test Cases ***\n")
    for caseid in caseids:
        casename = "TestCase-" + str(caseid).zfill(3)
        documentation = CaseBdd.objects.get(id=caseid).name
        content.append(casename + "\n")
        content.append("    [Documentation]    " + documentation + "\n")
        isrun = CaseBdd.objects.get(id=caseid).isrun
        content.append("    [Tags]    " + isrun + "\n")

        bus_key = 'bus_id'
        busids = list(CaseBddToBusiness.objects.filter(case_id=caseid).order_by('sort').values(bus_key))
        for bus in busids:
            bus_id = bus[bus_key]
            bus_name = Business.objects.get(id=bus_id).name
            content.append("    " + bus_name + "    " + str(caseid) + "\n")
        content.append("\n")
    return content


def createcase(casetag, suiteid):
    obj = SuiteName.objects.get(id=suiteid)
    suitename = obj.suitename
    funtag = obj.function.tag
    dir = os.path.join(case_dir, casetag, funtag, suitename)

    content = []
    content = content + getSetting(casetag, suiteid)
    content = content + getCase(suiteid)
    content.append("\n\n")
    with open(dir, "w", encoding='utf-8') as f:
        f.writelines(content)


def getSuite(casetag, funtag, suiteid):
    data = []
    caseids = [c['id'] for c in CaseBdd.objects.filter(suite_id=suiteid).order_by('sort').values('id')]
    for caseid in caseids:
        if casetag in [c.tag for c in CaseBdd.objects.get(id=caseid).tag.all()]:
            case = []
            case.append(caseid)
            case.append("TestCase-" + str(caseid).zfill(3))
            obj = CaseBdd.objects.get(id=caseid)
            case.append(obj.name)
            case.append(obj.isrun + "," + funtag)

            busids = [(b['id'], b['bus_id']) for b in
                      CaseBddToBusiness.objects.filter(case_id=caseid).order_by('sort').values('id', 'bus_id')]
            business = []
            for id, busid in busids:
                try:
                    params = [p.variable.name + "=" + p.value for p in
                              CaseBddToBusiness.objects.get(id=id).param.all()]
                except:
                    params = []
                business.append([Business.objects.get(id=busid).chinesename, ','.join(params)])
            case.append(business)
            case.append(obj.sort)
            data.append(case)
    return data


def getdata(**kwargs):
    casetag = kwargs['casetag'] if kwargs['casetag'] else 'InterfaceTest'
    funtag = kwargs['funtag'] if kwargs['funtag'] else 'all'
    dir = os.path.join(case_dir, casetag)

    if funtag == "all":
        funtags = list(filter(None, [y for y in os.listdir(dir)]))
    else:
        funtags = [funtag]
    data = []
    for tag in funtags:
        datatag = []
        tag_dir = os.path.join(dir, tag)
        suite = list(filter(None, [y if '.robot' in y else None for y in os.listdir(tag_dir)]))
        for suitename in suite:
            suiteid = SuiteName.objects.get(suitename=suitename).id
            cases = getSuite(casetag, tag, suiteid)
            if cases:
                datatag.append([suiteid, suitename, cases])
        if datatag:
            data = data + datatag
    return data


def getbusinesskeyall(bustag):
    dir = os.path.join(bus_dir, bustag)
    suite = list(filter(None, [y if '.robot' in y else None for y in os.listdir(dir)]))
    keys = []
    for suitename in suite:
        file_dir = os.path.join(dir, suitename)

        with open(file_dir, "r", encoding='utf-8') as f:
            readcontent = f.readlines()
        readcontent = [l.strip('\n') for l in readcontent]

        index = readcontent.index('*** Keywords ***')
        if index + 1 < len(readcontent):
            readkeys = list(filter(None, [readcontent[i] if not readcontent[i].startswith(' ', 0, 3) else None for i in
                                          range(index + 1, len(readcontent))]))
            keys = keys + readkeys
    return keys


def insertbusiness(file_dir, bustag, busid):
    content = []
    obj = Business.objects.get(id=busid)
    busname = obj.name
    data = "业务--" + Business.objects.get(name=busname).chinesename + "，初始化代码已生成！"
    if busname in getbusinesskeyall(bustag):
        data = "业务--" + Business.objects.get(name=busname).chinesename + "，已经存在，不需要初始化！"
    else:
        content.append(busname + "\n")
        content.append("    [Arguments]    ${caseid}\n")
        content.append("    [Documentation]    " + obj.chinesename + "\n")
        params = ['${userid}']
        try:
            vars = ["${" + Variable.objects.get(id=bv['var_id']).name + "}" for bv in
                    BusinessToVariable.objects.filter(bus_id=busid).order_by('sort').values('var_id')]
        except:
            vars = []
        params = params + vars
        content.append("    " + "    ".join(params) + "    getParams    ${caseid}    " + busname + "\n")
        content.append("    should be true    ${False}    代码还没有实现\n")
        content.append("\n")

    with open(file_dir, "a+", encoding='utf-8') as f:
        f.writelines(content)

    return data


def run_robot_cmd(user, tags):
    include = ' '
    if tags:
        include = ' --include ' + " --include ".join(tags) + " "

    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    cmd = "python3 -m  robot.run -d " + os.path.join(media_dir, "results") + " --exclude NotRun" + include + case_dir
    print(cmd)
    os.system(cmd)

    time_str = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    dir_path_1 = os.path.join(media_dir, 'results')
    dir_path_2 = os.path.join(media_dir, 'history', 'results-' + user + "-" + time_str + "-" + ".".join(tags))
    shutil.copytree(dir_path_1, dir_path_2)


def run_case_cmd(user, dir, casename):
    print(dir,casename)
    cmd = "python3 -m  robot.run -d " + os.path.join(media_dir, "results") + " --test " + casename + " " + dir
    print(cmd)
    os.system(cmd)

    time_str = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    dir_path_1 = os.path.join(media_dir, 'results')
    dir_path_2 = os.path.join(media_dir, 'history', 'results-' + user + "-" + time_str + "-" + casename)
    shutil.copytree(dir_path_1, dir_path_2)
