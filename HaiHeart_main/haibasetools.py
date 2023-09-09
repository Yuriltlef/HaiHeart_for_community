#   -*- coding: utf-8 -*-
#
#
# Mozilla Public License Version 2.0
# Copyright (c) 2023, Flepis


from . import haisettings
from .HaiErrors import *
import numbers
import math
import typing
import os
import sys
import time


def MAIN_VEC_TYPE_CHECKING(fuc):
    """
    检查必要运算语句(只在haisettings.HAI_MAIN_DEBUG==True时有效)\n
    """
    if haisettings.HAI_MAIN_DEBUG:
        def checker(self: "HaiVector", other: "HaiVector"):
            if fuc.__name__ == '__mul__':
                if not isinstance(other, numbers.Number):
                    raise TypeError
                return fuc(self, other)
            if type(self) is not HaiVector or type(other) is not HaiVector:
                raise TypeError
            if self.vectorLen != other.vectorLen:
                raise TypeError
            else:
                return fuc(self, other)

        return checker

    if not haisettings.HAI_MAIN_DEBUG:
        return fuc


def get_opposite_vector(vector: "HaiVector") -> "HaiVector":
    """
    求一个向量的相反向量，返回一个相反向量
    :param vector:
    :return:
    :rtype: HaiVector
    """
    alist = []
    for coordinate_tuple in vector:
        alist.append(-coordinate_tuple[1])
    return HaiVector(alist)


def get_hai_module(vector: "HaiVector") -> float:
    """
    求向量的模
    :rtype: float
    :param vector:
    :return: 
    """
    alist = []
    for sport_tuple in vector:
        alist.append(math.pow(sport_tuple[1], 2))
    return math.pow(sum(alist), 0.5)


# class MainVectorGetter:
#    """
#    获取向量属性的描述器
#    """
#
#    def __get__(self, instance: "HaiVector", owner=None) -> list[numbers.Number]:
#        if isinstance(instance, HaiVector):
#            return []


class HaiVector(object):
    """
    MainGame中的向量类
    是一个可迭代对象
    遍历返回tuple(坐标列表中的位置，坐标)
    例如：\n
    f = HaiVector([1,2,3])\n
    for i in f: print(i)\n
    输出：\n
    (0,1);(1,2);(2,3)\n
    支持向量加法，减法和点乘\n
    :+  -:向量线性加，减法；\n
    :*  @:向量数量积，点乘；\n
    支持一些增强赋值，如+=,-=,*=
    """

    # noinspection PyUnusedLocal
    def __init__(self, coordinate: list, *args: any) -> None:
        self.__coordinate = coordinate
        self.__index = 0
        self.vectorLen = len(self)
        self.module = get_hai_module(self)
        self.coordinate = self.__coordinate
        self.__slots__ = ['vectorLen', 'module', 'coordinate']

    def __iter__(self):
        return self

    def __next__(self) -> tuple[int, any]:
        if self.__index < self.vectorLen:
            self.__index += 1
            return self.__index - 1, self.__coordinate[self.__index - 1]

        if self.__index == self.vectorLen:
            self.__index = 0
            raise StopIteration

    def __len__(self):
        return len(self.__coordinate)

    @MAIN_VEC_TYPE_CHECKING
    def __add__(self, other: "HaiVector") -> "HaiVector":
        for __coordinate in other:
            self.__coordinate[__coordinate[0]] += __coordinate[1]
        return HaiVector(self.__coordinate)

    @MAIN_VEC_TYPE_CHECKING
    def __sub__(self, other: "HaiVector") -> "HaiVector":
        return self + get_opposite_vector(other)

    @MAIN_VEC_TYPE_CHECKING
    def __matmul__(self, other: "HaiVector") -> float:
        alist = []
        for __index in range(self.vectorLen):
            alist.append(self.__coordinate[__index] * other.coordinate[__index])
        return float(sum(alist))

    @MAIN_VEC_TYPE_CHECKING
    def __iadd__(self, other: "HaiVector") -> "HaiVector":
        _self = self
        _self = self + other
        return _self

    @MAIN_VEC_TYPE_CHECKING
    def __isub__(self, other: "HaiVector") -> "HaiVector":
        _self = self
        _self = self - other
        return _self

    @MAIN_VEC_TYPE_CHECKING
    def __eq__(self, other: "HaiVector") -> bool:
        if self.coordinate == other.coordinate:
            return True

    @MAIN_VEC_TYPE_CHECKING
    def __mul__(self, other: numbers.Number) -> "HaiVector":
        alist = []
        for __index in range(self.vectorLen):
            alist.append(self.__coordinate[__index] * other)
        return HaiVector(alist)

    def __imul__(self, other: numbers.Number) -> "HaiVector":
        _self = self
        _self = self * other
        return _self

    def __repr__(self) -> str:
        return f"<A Vector object in {hex(id(self))},\nThe" \
               f" coordinate list is {str(self.__coordinate)},\n" \
               f"From \n{__file__} {type(self)}>"

    def __hash__(self) -> int:
        return hash(str(self))

    def __abs__(self) -> float:
        return self.module


# noinspection PyUnusedLocal
class HaiSystemOut(object):
    """
    格式化输出结果
    """

    def __init__(self, input_type: any = None,
                 judgment_fuc: typing.Callable = None,
                 stream_head_chooser_kwargs: dict = {},
                 type_chooser_kwargs: dict = {},
                 **kwargs):

        self.__input_type = input_type

        self.__stream_head = self.stream_head_chooser(input_type=input_type, judgment_fuc=judgment_fuc,
                                                      **stream_head_chooser_kwargs)

        self.__type = self.type_chooser(input_type=input_type,
                                        judgment_fuc=judgment_fuc,
                                        **type_chooser_kwargs)

        self.__format = "[{}][{}][{}][{}]"

        self.__logs = ""

    @staticmethod
    def stream_head_chooser(input_type: any = None, judgment_fuc: typing.Callable = None, **kwargs) -> str:
        """
        judgment_fuc为可调用类型，且应该返回对输入类型判断结果\n
        返回值应该为一段有意义的字符串\n
        如果未提供judgment_fuc，默认返回"HaiMain"\n
        安全警告：judgment_fuc永远不应该执行钩子类型，以防止意外的执行或注入代码
        """
        if judgment_fuc:
            return judgment_fuc(input_type, **kwargs)

        else:
            return "HaiMain"

    @staticmethod
    def type_chooser(input_type: any = None, judgment_fuc: typing.Callable = None, **kwargs) -> str:
        """
        judgment_fuc为可调用类型，且应该返回对输入类型判断结果\n
        返回值应该为一段有意义的字符串\n
        如果未提供judgment_fuc，默认返回"INFO"\n
        安全警告：judgment_fuc永远不应该执行钩子类型，以防止意外的执行或注入代码
        """
        if judgment_fuc:
            return judgment_fuc(input_type, **kwargs)

        else:
            return "INFO"

    def thread_name(self) -> str:
        """
        获得当前进程的名称
        """
        return __name__

    def log_out(self, log_text: str = '') -> None:
        """
        打印日志
        """
        __log = "[{}][{}][{}][{}]".format(time.strftime("%Y %B %d %H:%M:%S"), self.__stream_head,
                                          self.thread_name(),
                                          self.__type) + log_text
        print(__log)

        self.__logs += (__log + log_text + "\n")

    def logs_writer(self, path: str) -> None:
        """
        写入日志文件
        """
        with open(path, "a+") as file:
            file.write(self.__logs)



