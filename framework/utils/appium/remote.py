# -*- coding: UTF-8 -*-

"""
File Name:      remote
Author:         zhangwei04
Create Date:    2018/1/19
"""
from appium import webdriver


class AppiumRemote(webdriver.Remote):
    """
    Appium 链接session对象
    """
    def __init__(self, command_executor='http://127.0.0.1:4723/wd/hub', desired_capabilities=None,
                 browser_profile=None, proxy=None, keep_alive=False):
        super(AppiumRemote, self).__init__(command_executor, desired_capabilities, browser_profile, proxy, keep_alive)

    def execute(self, driver_command, params=None):
        return super(AppiumRemote, self).execute(driver_command, params)
