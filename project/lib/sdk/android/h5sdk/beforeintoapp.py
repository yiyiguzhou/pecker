# -*- coding: UTF-8 -*-

"""
File Name:      intogame
Author:         fuhongzi
Create Date:    2018/5/9
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource


class Beforeintoapp(object):
    def __init__(self, target):
        self.target = target
        self.data = target.data
        self.device = target.device

    """
           滑动广告
           Returns:
               True: 进入成功
               False：进入失败
    """
    def sllide_advertising(self,game_text=''):
        time.sleep(3)
        try:
            self.find_element_by_id('tourist',timeout=3).click()
        except:
            g_logger.error('guest login failed:'+ game_text)
            return False
        return True