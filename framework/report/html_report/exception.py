# -*- coding: UTF-8 -*-

"""
File Name:      exception
Author:         zhangwei04
Create Date:    2017/12/25
"""
import subprocess


class FileNotFound(Exception):
    """
    文件没找到异常
    """
    pass


class ParamaterError(Exception):
    """
    参数错误异常
    """
    pass


class ParameterTypeError(Exception):
    """
    参数类型错误异常
    """
    pass


class InstanceError(Exception):
    """实例异常"""
    pass


class AssertException(Exception):
    """断言异常"""
    pass


class DevicesTypeError(Exception):
    """设备类型异常，若设备不是Android或IOS，则抛出异常"""
    pass


class TimeoutExpired(subprocess.TimeoutExpired):
    """线程超时异常"""
    pass


class DeviceNotFound(Exception):
    """设备没找到异常"""
    pass


class DeviceUnauthorized(Exception):
    """设备没有授权异常"""

    def __init__(self, dev_name):
        self.dev_name = dev_name

    def __str__(self):
        return "devices: '%s' are unauthorized" % self.dev_name


class TimeoutException(Exception):
    """超时异常"""
    pass


class AttributeNotSet(Exception):
    """属性没被设置异常"""
    pass
