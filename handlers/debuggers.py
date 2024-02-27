import logging
from collections import Counter
from pprint import pprint

from mitmproxy.http import HTTPFlow

global_counter = Counter()


def debugger_method(flow: HTTPFlow):
    logging.info(f"Intercepted request to {flow.request}")
    return flow


def coder_byte(flow: HTTPFlow):
    # Using mutable default arguments as feature, storing the global counter
    url = flow.request.path
    global_counter[url] += 1
    pprint(dict(global_counter))
    return flow
