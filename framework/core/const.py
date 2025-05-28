# -*- coding: UTF-8 -*-

"""
File Name:      const
Author:         zhangwei04
Create Date:    2018/3/1
"""


class Const(object):
    """常量类，包含一些常量成员"""
    def __init__(self):
        self.__sys_windows = 0
        self.__sys_linux = 1
        self.__sys_mac = 2


    @property
    def SYSTEM_WINDOWS(self):
        """window平台常量值"""
        return self.__sys_windows

    @property
    def SYSTEM_LINUX(self):
        """linux平台常量值"""
        return self.__sys_linux

    @property
    def SYSTEM_MAC(self):
        """mac平台常量值"""
        return self.__sys_mac


class ResultStatus(object):
    """用例执行结果常量"""
    def __init__(self):
        self.__passed = 0
        self.__failed = 1
        self.__error = 2
        self.__block = 3

    @property
    def values(self):
        """返回变量集合"""
        return [self.__passed, self.__failed, self.__error, self.__block]

    @property
    def PASSED(self):
        """通过"""
        return self.__passed

    @property
    def FAILED(self):
        """失败"""
        return self.__failed

    @property
    def ERROR(self):
        """错误"""
        return self.__error

    @property
    def BLOCK(self):
        """未执行"""
        return self.__block

    def get_desc(self, status):
        """获取状态中文描述"""
        status_desc = None
        if status == self.__passed:
            status_desc = "passed"
        elif status == self.__failed:
            status_desc = "failed"
        elif status == self.__error:
            status_desc = "error"
        elif status == self.__block:
            status_desc = "block"

        return status_desc


reslut_status = ResultStatus()
