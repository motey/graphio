from graphio.objects.datacontainer import Container
from typing import Callable
import multiprocessing


class MpManager:
    """

    Args:
        Container ([type]): [description]
    """

    def __init__(self):
        self.container = Container()

    def set_parsers(self, parser_func: Callable, params: list[set], concurent_worker_count=None):
        if concurent_worker_count is None:
            concurent_worker_count = multiprocessing.cpu_count() - 1

    def _add_object(self, object):
        pass
