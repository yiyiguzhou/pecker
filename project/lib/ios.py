# -*- coding: UTF-8 -*-

"""
File Name:      ios
Author:         zhangwei04
Create Date:    2018/5/21
"""
from .base_interface import BaseInterface


class IOS(BaseInterface):
    def __init__(self, target=None, ele_conf_name=None):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
