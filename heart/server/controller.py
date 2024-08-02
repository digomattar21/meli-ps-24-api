from json import dumps, loads
from flask.views import MethodView
from flask import request, make_response


class BaseController(MethodView):

    def getBodyBytes(self):
        return request.get_data()

    def getBody(self):
        return request.get_data().decode("utf-8")

    def getJsonBody(self):
        try:
            return loads(request.get_data().decode("utf-8"))
        except:
            return {}

    def getQuery(self):
        return request.args

    def getParameter(self, parameter, default=""):
        return request.args.get(parameter, default)

    def getHeaders(self):
        return request.headers

    def userAgent(self):
        return request.headers.get("User-Agent")

    def sendJson(self, obj, headers=None, status=None):
        headers = headers or {}
        headers.update({"Content-Type": "application/json"})
        status = status or (400 if "errors" in obj else 200)
        return self.sendContent(content=dumps(obj), headers=headers, status=status)

    def sendContent(self, content="", headers=None, status=200):
        headers = headers or {}
        headers["Access-Control-Allow-Origin"] = "*"
        return make_response(content, status, headers)
