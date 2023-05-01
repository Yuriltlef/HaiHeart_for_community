#   -*- coding: utf-8 -*-
#
#
# BSD 3-Clause License
#
# Copyright (c) 2023, Flepis


import haisettings
import numbers
import math
import os
import sys
import time
from HaiErrors import *


def MAIN_VEC_TYPE_CHECKING(fuc):
    """
    检查必要运算语句(只在haisettings.HAI_MAIN_DEBUGE==True时有效)\n
    """
    if haisettings.HAI_MAIN_DEBUGE:
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

    if not haisettings.HAI_MAIN_DEBUGE:
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


def del_unsupported_attr(instance: any, **kwargs) -> dict[str, any]:
    """
    动态地删除子类中不需要的属性
    :param instance:
    :param kwargs:
    :return:
    """
    instance.__dict__[kwargs]


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

    def __init__(self, coordinate: list, *args: any) -> None:
        self.__coordinate = coordinate
        self.__index = 0
        self.vectorLen = len(self)
        self.module = get_hai_module(self)
        self.coordinate = self.__coordinate
        self.__slots__ = ['vectorLen', 'module', 'coordinate']

    def __init_subclass__(cls, /, hook=None, tags: dict = None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.direction_vector = HaiVector
        if hook:
            hook(cls, **tags)

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


class HaiLine(HaiVector):
    """
    定义线段对象
    继承自HaiVector
    """

    def __init__(self, start_coordinate: list, end_coordinate: list):
        super().__init__([(x1 - x2) for x1, x2 in zip(start_coordinate, end_coordinate)])
        self.name = 1

    def __len__(self):
        return len(self.__coordinate)

    def __add__(self, other: "HaiVector") -> "HaiVector":
        return NotImplemented

    def __sub__(self, other: "HaiVector") -> "HaiVector":
        return NotImplemented

    def __matmul__(self, other: "HaiVector") -> float:
        return NotImplemented

    def __iadd__(self, other: "HaiVector") -> "HaiVector":
        return NotImplemented

    def __isub__(self, other: "HaiVector") -> "HaiVector":
        return NotImplemented

    def __eq__(self, other: "HaiVector") -> bool:
        return NotImplemented

    def __mul__(self, other: numbers.Number) -> "HaiVector":
        return NotImplemented

    def __imul__(self, other: numbers.Number) -> "HaiVector":
        return NotImplemented

    def __repr__(self) -> str:
        return f"<A Line object in {hex(id(self))},\nThe" \
               f" coordinate list is {str(self.__coordinate)},\n" \
               f"From \n{__file__} {type(self)}>"

    def __hash__(self) -> int:
        return hash(str(self))

    def __abs__(self) -> float:
        return self.module
