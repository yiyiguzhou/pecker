# -*- coding: UTF-8 -*-

"""
File Name:      MenuEdit
Author:         zhangwei04
Create Date:    2018/10/22
"""
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QMouseEvent


class MenuEdit(QMenu):
    """右击是菜单选择栏"""
    def __init__(self):
        super().__init__()
        # self.menu = QMenu()
        self.eidt_action = self.addAction("编辑")
        self.add_action = self.addAction("添加")
        self.del_action = self.addAction("删除")

    def reg_ac(self, ac_name, ac_desc):
        """注册action
        Args:
            ac_name: action属性名称
            ac_desc: action 属性描述
        """
        action = self.addAction(ac_desc)
        setattr(self, ac_name, action)

