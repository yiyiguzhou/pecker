# -*- coding: UTF-8 -*-

"""
File Name:      pingback
Author:         zhangwei04
Create Date:    2018/8/23
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from framework.utils.iMitmProxy.imitm import IMitm


class Pingback(Android):
    def __init__(self, target):
        super().__init__(target=target)

        self.target = target
        self.data = target.data
        self.device = target.device
        self._imitm = IMitm()

    def start_catch(self):
        self._imitm.start()

    def stop_catch(self):
        self._imitm.stop()
        self._imitm.report()

    def into_game_center(self):
        """
        从推荐页面中基线进入游戏
        Returns:
            True：进入成功
            False：进入失败
        """
        time.sleep(10)
        for i in range(3):
            try:
                self.device.click_by_id(self.conf.base_recommend.id, timeout=5, mitm=self._imitm)
                time.sleep(5)
                self.device.click_by_xpath(self.conf.base_recommend_gamecenter.xpath, timeout=5, mitm=self._imitm, index_list=[1, 2, 3, 4], no_order_index=[1, 2, 3, 4], desc="点击游戏中心")
                self.device.find_element_by_id(self.conf.gamecenter_newgame.id, timeout=5)
                break
            except Exception as e:
                g_logger.info(str(e))
                return False
        return True

    def gamecenter_into_new_game(self):
        """
        从游戏中心进入新游页
        Returns:
            True：进入成功
            False：进入失败
        """
        try:
            self.device.click_by_id(self.conf.gamecenter_newgame.id, timeout=5, mitm=self._imitm,
                                   index_list=[i for i in range(5, 12)], no_order_index=[5, 6, 11, 7], desc="点击新游")
        except:
            return False
        return True