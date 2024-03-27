#   -*- coding: utf-8 -*-
#
#
# Mozilla Public License Version 2.0
# Copyright (c) 2023, Flepis

import multiprocessing as pyprocess
import typing
from multiprocessing import Pipe
import math
import numpy
import time
import os
import sys
from . import GaCtrlFlow, GaProces

GA_MAIN_THREADING_POOL = {}


class GaPipe:
    """实现进程间数据便捷访问"""


class GaThreading(pyprocess.Process):
    """伪装成线程的类/n
    为什么不直接使用Threading库呢？/n
    理由很简单，因为GIL/n
    这个模块对Proces进行了封装，方便了各个进程间的数据访问/n
    一般情况下推荐使用这个类而不是GaProces
    """

    def __init__(self,
                name: str,
                target_fuc: typing.Callable = None,
                kind=None,
                pool=GA_MAIN_THREADING_POOL,
                weight=1,
                **kwargs):
        super().__init__(self, target=target_fuc, **kwargs)
        self.ga_game = name
        self.pool = pool
        self.target_fuc = target_fuc
        GA_MAIN_THREADING_POOL[f'{self.pid}' + self.ga_game] = self
        self.clock_pool = {}
