# coding=utf-8

import json
import requests
import re
from TestCase.Library.SqlDjango import SqlDjango
from Config.project import url


class LibRequest(object):
    def __init__(self):
        self.url = url

    def getHeader(self, userid):
        sql = "SELECT token,reqchannel FROM `tag_user` WHERE id=" + str(userid)
        query = SqlDjango().execute_sql(sql)
        headers = {"Authorization": query[0][0], "ReqChannel": query[0][1]}
        return headers

    def getResponse(self, userid, mode, path, params=None):
        headers = self.getHeader(userid)
        print("Headers = ", headers)

        uri = path
        if params:
            pattern = re.compile(r'{\w*}')
            path_params = re.findall(pattern, path)
            for p in path_params:
                key = p[1:-1]
                uri = uri.replace(str(p), str(params[key]))
                del params[key]

        sql = "SELECT id,file_id FROM `yaml_path` WHERE path='" + path + "' and mode='" + mode + "'"
        query = SqlDjango().execute_sql(sql)
        id = query[0][0]
        file_id = query[0][1]
        sql = "SELECT basepath FROM `yaml_file` WHERE id=" + str(file_id)
        basepath = SqlDjango().execute_sql(sql)[0][0]
        if basepath in path:
            basepath = ""
        curl = self.url + basepath + uri
        print("Params = ", params)

        response = self._getRespMode(id, mode, curl, headers, params)
        print("URL = ", response.url)
        resp_text = response.text
        if "Content-Type" in response.headers:
            if "image/jpeg" in response.headers['Content-Type']:
                resp_text = "image"
        print("Resp = ", resp_text)
        return self._getRespContent(response)

    def _getRespMode(self, id, mode, curl, headers, params):
        if mode == "get":
            response = requests.get(curl, params=params, headers=headers, verify=False)
        elif mode == "post":
            headers['Content-Type'] = "application/json"
            response = requests.post(curl, data=json.dumps(params), headers=headers, verify=False)
        elif mode == "put":
            sql = "SELECT method FROM `yaml_param` WHERE path_id=" + str(id)
            param_method = [q[0] for q in SqlDjango().execute_sql(sql)]
            if "body" in param_method:
                headers['Content-Type'] = "application/json"
                response = requests.put(curl, data=json.dumps(params), headers=headers, verify=False)
            else:
                response = requests.put(curl, params=params, headers=headers, verify=False)
        return response

    def _getRespContent(self, response):
        code = response.status_code
        content = response.content
        if code == 200:
            try:
                content = json.loads(content)
            except:
                print("json loads failure")
        return (code, content)


if __name__ == '__main__':
    LibRequest().getResponse(1,'put','/users/subjects',  params={'subjectid': 17})
