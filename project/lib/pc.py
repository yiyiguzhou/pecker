# -*- coding: UTF-8 -*-

"""
File Name:      pc
Author:         zhangwei04
Create Date:    2019/7/12
"""
import os
import time
from .base_interface import BaseInterface
from framework.core.resource import g_resource
from framework.logger.logger import g_logger
from project.conf.elements_conf.configure import ElementConfig, AccountConfig


class PC(BaseInterface):
    def __init__(self, target, ele_conf_name=None):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
        self.installed_app_dict = dict()    # 自动化过程中，安装的app
        self.conf_img_dir = os.path.join(g_resource['project_path'], 'conf', 'img')
        self._window_size = None
        self.app_conf = ElementConfig("app")
        self.account_conf = AccountConfig()     # 账户配置文件