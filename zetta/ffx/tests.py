from unittest import TestCase

from zetta.ffx import route
from zetta.ffx.router import Router
from zetta.ffx.runner import ApplicationRunner
from zetta.common import Logger

logger = Logger.get_logger("FFXTest")


class CalculatorRouter(Router):
    @route(url="/add/<a>/<b>", methods=["GET"])
    def add(self, a, b):
        return str(int(a) + int(b))

    @route(url="/multiply", methods=["GET", "POST"])
    def multiply(self, params):
        a = int(params["a"])
        b = int(params["b"])
        return str(a * b)


class FFXTest(TestCase):
    def get_svc(self):
        runner = ApplicationRunner("FFXTest", host="0.0.0.0", port=21000, debug=True,
                                   key="A0Zr98j/3yX R~XHH!jmN]LWX/,?RS")
        runner.register(CalculatorRouter())
        return runner

    def test_startServer(self):
        runner = self.get_svc()
        runner.run()
