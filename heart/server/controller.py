from json import JSONDecodeError, dumps, loads

from flask import make_response, request
from flask.views import MethodView


class BaseController(MethodView):

    def get_body_bytes(self):
        return request.get_data()

    def get_body(self):
        return request.get_data().decode("utf-8")

    def get_json_body(self):
        try:
            return loads(request.get_data().decode("utf-8"))
        except JSONDecodeError:
            return {}

    def get_query(self):
        return request.args

    def get_parameter(self, parameter, default=""):
        return request.args.get(parameter, default)

    def get_headers(self):
        return request.headers

    def user_agent(self):
        return request.headers.get("User-Agent")

    def send_json(self, obj, headers=None, status=None):
        headers = headers or {}
        headers.update({"Content-Type": "application/json"})
        status = status or (400 if "errors" in obj else 200)
        return self.send_content(content=dumps(obj), headers=headers, status=status)

    def send_content(self, content="", headers=None, status=200):
        headers = headers or {}
        headers["Access-Control-Allow-Origin"] = "*"
        return make_response(content, status, headers)
