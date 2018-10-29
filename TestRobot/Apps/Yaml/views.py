import json
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from Config.directory import yaml_dir, yaml_names
from Config.project import projectName
from Util.ParserSwagger import ParserSwagger
from Yaml.models import File, Tag, Param, Path

param_dict = {"project": projectName}


def yaml(request):
    param_dict['title'] = '接口文档'
    if str(request.user) == "admin":
        return render(request, 'yaml.html', param_dict)
    else:
        return HttpResponseRedirect("/")


def editfile(request):
    data = []
    for yaml in yaml_names:
        p = ParserSwagger(os.path.join(yaml_dir, yaml))
        try:
            File.objects.get(name=yaml)
            File.objects.filter(
                name=yaml
            ).update(
                host=p.host,
                basepath=p.basePath
            )
        except:
            data.append(yaml)
            File.objects.create(
                name=yaml,
                host=p.host,
                basepath=p.basePath
            )

    resp = {"success": True, "filenames": ",".join(data)}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def edittag(request):
    data = []
    for yaml in yaml_names:
        p = ParserSwagger(os.path.join(yaml_dir, yaml))
        id = File.objects.get(name=yaml).id
        for tag, description in p.tags.items():
            try:
                Tag.objects.get(name=tag, file_id=id)
                Tag.objects.filter(
                    name=tag,
                    file_id=id
                ).update(
                    description=description
                )
            except:
                data.append(tag)
                Tag.objects.create(
                    name=tag,
                    file_id=id,
                    description=description
                )

    resp = {"success": True, "filenames": ",".join(data)}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def editpath(request):
    data = []
    for yaml in yaml_names:
        p = ParserSwagger(os.path.join(yaml_dir, yaml))
        id = File.objects.get(name=yaml).id
        for path in p.paths:
            for mode in p.get_path_modes(path):
                tag = p.get_path_tags(path)[0]
                tag_id = Tag.objects.get(name=tag).id
                summary = p.paths_data[path][mode]['summary']
                description = p.paths_data[path][mode].get('description','')
                resp = p.paths_data[path][mode]['responses']['200']
                try:
                    Path.objects.get(path=path, mode=mode, file_id=id)
                    Path.objects.filter(
                        path=path,
                        mode=mode,
                        file_id=id
                    ).update(
                        tag_id=tag_id,
                        summary=summary,
                        description=description,
                        resp=resp
                    )
                except:
                    data.append(path + "--" + mode)
                    Path.objects.create(
                        path=path,
                        mode=mode,
                        file_id=id,
                        tag_id=tag_id,
                        summary=summary,
                        description=description,
                        resp=resp
                    )

    resp = {"success": True, "filenames": ",".join(data)}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def editparam(request):
    data = []
    for yaml in yaml_names:
        p = ParserSwagger(os.path.join(yaml_dir, yaml))
        id = File.objects.get(name=yaml).id
        for path in p.paths:
            for mode in p.get_path_modes(path):
                path_id = Path.objects.get(path=path, mode=mode, file_id=id).id
                parameters = p.paths_data[path][mode]['parameters']
                for params in parameters:
                    name = list(params['name'].keys())[0]
                    method = params['method']
                    value = params['name'][name]
                    if method == 'body':
                        ptype = 3
                    elif isinstance(params['name'][name], int):
                        ptype = 0
                    elif isinstance(params['name'][name], str):
                        ptype = 1
                    elif isinstance(params['name'][name], bool):
                        ptype = 2
                    else:
                        ptype = 4
                    required = 1 if params.get('required', True) else 0
                    description = params.get('description', '')

                    try:
                        Param.objects.get(path_id=path_id, name=name)
                        Param.objects.filter(
                            path_id=path_id,
                            name=name
                        ).update(
                            value=value,
                            method=method,
                            ptype=ptype,
                            required=required,
                            description=description
                        )
                    except:
                        data.append(path + "--" + name)
                        Param.objects.create(
                            path_id=path_id,
                            name=name,
                            value=value,
                            method=method,
                            ptype=ptype,
                            required=required,
                            description=description
                        )

    resp = {"success": True, "filenames": ",".join(data)}
    return HttpResponse(json.dumps(resp), content_type="application/json")
