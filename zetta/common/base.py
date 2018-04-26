import inspect
from datetime import datetime

import sys

PRIMITIVES = (int, float, bool, str, bytearray, classmethod, complex, enumerate, unicode, long, datetime,)
IDENTITY = lambda x: x


def deconstruct(max_depth, obj):
    if max_depth == 0 or obj is None or isinstance(obj, PRIMITIVES + (Struct, )) or inspect.isroutine(obj):
        return obj
    elif max_depth > 0 and isinstance(obj, dict):
        result = Struct()
        for k, v in obj.iteritems():
            setattr(result, k, deconstruct(max_depth - 1, v))
        return result
    elif max_depth > 0 and (isinstance(obj, list) or isinstance(obj, tuple)):
        return [deconstruct(max_depth - 1, i) for i in obj]
    else:
        return obj


class Struct(object):
    def __init__(self, max_depth=0, **states):
        self.update(max_depth=max_depth, **states)

    def update(self, max_depth=sys.maxint, **states):
        for k, v in states.items():
            setattr(self, k, deconstruct(max_depth, v))
        return self

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return reduce(lambda x, y: x + hash(y[1]), inspect.getmembers(self), 0)


class StructFactory:
    """
    IMPLEMENTATION NOTES: constructs struct object with rules from another struct (src)
    - rule format:
      - (a, f) --> self.a = f(src.a)
      - (a, f, bool) --> self.a = f(pop.a)
      - (a, b) --> self.a = IDENTITY(src.b)
      - (a, b, bool) --> self.a = IDENTITY(src.pop(b))
      - (a, b, f) --> self.a = f(src.b)
      - (a, b, f, bool) --> self.a = f(src.pop(b))
    """
    @classmethod
    def construct(cls, src, self=None, rules=None):
        self = self or Struct()
        i_dict = src if isinstance(src, dict) else src.__dict__.copy()
        if rules:
            for rule in rules:
                rule = list(rule)
                if not isinstance(rule[1], basestring):
                    if len(rule) == 2:
                        rule.append(True)
                    rule.append(rule[2])
                    rule[2] = rule[1]
                    rule[1] = rule[0]
                if isinstance(rule[2], bool):
                    rule.append(rule[2])
                    rule[2] = IDENTITY
                if len(rule) < 3 or rule[2] is None:
                    rule.append(IDENTITY)
                if len(rule) < 4 or rule[3] is None:
                    rule.append(True)
                a, b, fn, pop = rule
                b_val = i_dict.pop(b, None) if pop else i_dict.get(b, None)
                setattr(self, a, fn(b_val))
        return self.update(max_depth=127, **i_dict)


class AppResponse(Struct):
    data = None
    headers = None
    code = None

    @classmethod
    def return_200(cls, data, headers=None):
        headers = headers or {}
        return cls(data=data, headers=headers, code=200)

    @classmethod
    def return_500(cls, data, headers=None):
        headers = headers or {}
        return cls(data=data, headers=headers, code=500)


class PageMeta(Struct):
    title = None
    notifications = None
    description = None
    keywords = None


class Form(Struct):
    data = None
    errors = None


class RequestContext:
    url = None
    charset = None
    content_type = None
    cookies = None
    host = None
    files = None
    form = None
    args = None
    method = None
    user_agent = None
    is_json = False
    json = None

    def __init__(self, request):
        self.url = request.url
        self.charset = request.charset
        self.content_type = request.content_type
        self.cookies = request.cookies
        self.host = request.host
        self.files = request.files
        self.form = request.form
        self.args = request.args
        self.method = request.method
        self.user_agent = str(request.user_agent)
        self.json = request.json
        self.is_json = request.is_json