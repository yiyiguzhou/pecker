# -*- coding: UTF-8 -*-

"""
File Name:      action_chains
Author:         zhangwei04
Create Date:    2019/7/11
"""
from selenium.webdriver import ActionChains


class IActionChains(ActionChains):
    """重载ActionChains"""
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.perform()
        self.reset_actions()