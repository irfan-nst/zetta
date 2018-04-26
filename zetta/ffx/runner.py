from inspect import getmembers, ismethod

import jinja2
from flask import Flask

from zetta.common import Struct, Logger


class ApplicationRunner:
    class Config(Struct):
        host = None
        port = None
        key = None
        debug = False

    def __init__(self, app_name, **config):
        self.config = self.Config(**config)

        self.logger = Logger.get_logger("Main")
        self.app_name = app_name

        self.flask_app = Flask(__name__)
        my_loader = jinja2.ChoiceLoader([
            self.flask_app.jinja_loader,
            jinja2.FileSystemLoader(("/templates",)),
        ])
        self.flask_app.jinja_loader = my_loader
        self.flask_app.add_route = self.__add_route
        if self.config.key:
            self.flask_app.secret_key = self.config.key

    def register(self, router):
        functions = [o[1] for o in getmembers(router) if ismethod(o[1]) and o[1].__dict__.pop("route", False)]
        for func in functions:
            rules = func.__dict__.get("route_info",)
            error_handler = rules.pop("error_handler", False)
            if error_handler:
                self.logger.info("Registering handler: %s (%s)" % (func.__name__, "E"))
                self.flask_app.errorhandler(error_handler)(func)
            else:
                url = rules.pop('url')
                if isinstance(url, list):
                    for i in url:
                        self.__add_route(func, i, **rules)
                else:
                    self.__add_route(func, url, **rules)

    def __add_route(self, decorator, url, **rules):
        self.logger.info("Registering handler: %s (%s)" % (decorator.__name__, url))
        self.flask_app.route(url, **rules)(decorator)

    def run(self):
        self.logger.info("Starting app: " + self.app_name)
        self.logger.info("Hosted on: " + self.config.host + ":" + str(self.config.port))

        # Start flask
        self.flask_app.run(host=self.config.host, port=self.config.port, debug=self.config.debug)
