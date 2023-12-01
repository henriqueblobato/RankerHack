import logging

from mitmproxy.http import HTTPFlow


def debugger_method(flow: HTTPFlow):
    logging.info(f"Intercepted request to {flow.request}")
    return flow
