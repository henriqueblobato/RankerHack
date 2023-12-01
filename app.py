import logging
import re
from functools import cached_property

import yaml
from mitmproxy import http

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()],
)


class CustomProxy:
    def __init__(self, config_file='config.yml'):
        self.config = self.load_config(config_file)
        self.handlers = self.load_handlers()
        self.drop_paths = self.config.get('drop_paths', [])
        logging.info(f"Loaded handlers: {self.handlers}")

    @cached_property
    def handler_paths(self):
        return list(self.handlers.keys())

    def load_config(self, config_file):
        with open(config_file) as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def load_handlers(self):
        handlers = {}
        for conf_dict in self.config.get('paths', {}):
            handler_name = conf_dict.get('url_path')
            handlers[handler_name] = self.load_handler(conf_dict.get('handler'))
            handlers[handler_name].config = conf_dict
        return handlers

    def load_handler(self, handler):
        module_name, function_name = handler.rsplit('.', 1)
        module = __import__(module_name, fromlist=[function_name])
        return getattr(module, function_name)

    def request_in_handlers_path(self, request_path):
        match = re.search('|'.join(self.handler_paths), request_path)
        if not match:
            return None
        return self.handlers[match.group()]

    def response(self, flow: http.HTTPFlow):
        if flow.request.path in self.drop_paths:
            logging.info(f"Dropping request to {flow.request.path}")
            return

        handler = self.request_in_handlers_path(flow.request.path)
        if handler:
            logging.info(f"Intercepting request to {flow.request.path} using {handler.config}")
            return handler(flow)

        return flow


addons = [CustomProxy()]

if __name__ == '__main__':
    from mitmproxy.tools.main import mitmdump

    mitmdump(['-p', '8081', '-s', __file__])
