# -*- coding: UTF-8 -*-

"""
File Name:      login
Author:         zhangwei04
Create Date:    2019/7/19
"""
from abc import ABCMeta, ABC, abstractmethod


class BaseLogin(metaclass=ABCMeta):

    """登录基类"""
    @abstractmethod
    def password_login(self):
        """密码登录"""
        pass

    @abstractmethod
    def sms_login(self):
        """短信登录"""
        pass

    @abstractmethod
    def qq_login(self):
        """QQ登录"""
        pass

    @abstractmethod
    def wechat_login(self):
        """微信登录"""
        pass
