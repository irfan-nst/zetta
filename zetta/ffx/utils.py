import inspect

from flask import request, Response

from zetta.common import Logger, RequestContext

logger = Logger.get_logger("CommonApp")


def parse_param(request):
    result = None
    sanitize = lambda x: None if x is None or x == '' else x
    if request.is_json:
        return request.json
    if request.method == "POST":
        result = [(i, sanitize(request.form.get(i, None))) for i in request.form]
    elif request.method == "GET":
        result = [(i, request.args.get(i, '')) for i in request.args]

    # if raise_on_empty and (not (result and all([x[1] is not None and x[1] is not "" for x in result]))):
    #     raise AssertionError("Some value are empty.")
    return dict(result)


def route(**rules):
    def wrapper(f):
        def wrapper2(self, *args, **kwargs):
            """
            :type self: zetta.ffx.api.Router
            """
            try:
                func_args = inspect.getargspec(f).args
                request_context = RequestContext(request)
                if "context" in func_args:
                    kwargs["context"] = request_context
                if "params" in func_args:
                    kwargs["params"] = parse_param(request_context)
                result = f(self, *args, **kwargs)
                if isinstance(result, Response):  # A flask response. Should not use send_response.
                    return result
                return self.send_response(result)
            except Exception, e:
                return self.send_response("Exception caught: " + str(e))

        wrapper2.__dict__ = f.__dict__
        wrapper2.__dict__.update(route=True, route_info=rules)
        wrapper2.__name__ = f.__name__
        wrapper2.func_args = inspect.getargspec(f).args
        return wrapper2
    return wrapper