from flask import make_response, render_template

from zetta.common import Struct
from utils import route


class Router:
    class Config(Struct):
        pass

    def __init__(self, **config):
        self.config = self.Config(**config)

    def send_response(self, result, headers=None, code=200):
        headers = headers or {}
        response = make_response(str(result), code)
        for k, v in headers.iteritems():
            response.headers[k] = v
        return response

    def render(self, template_file, **context):
        return render_template(template_file, app=self.config, **context)

    @route(url="/whoami", methods=["GET"])
    def whoami(self):
        with open("version.txt") as f:
            return f.read()
