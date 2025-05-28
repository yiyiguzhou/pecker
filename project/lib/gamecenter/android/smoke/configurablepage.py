# -*- coding: UTF-8 -*-

"""
File Name:      configurablepage
Author:         gufangmei_sx
Create Date:    2018/8/14
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from project.lib.gamecenter.android.smoke.common import Common


class Configurablepage(Common):
    """可配置页"""
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android')

        self.target = target
        self.data = target.data
        self.device = target.device

    def into_bottom_h5_game(self):
        """进入底部栏可配置页面
         Returns:
            True: 进入成功
            False：进入失败
         """
        try:
            self.device.click_by_id(self.conf.gamecenter_bottom_configurable.id, timeout=5, desc="点击底部可配置按钮")
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏中心']", timeout=5)
        except:
            return False
        return True

    def h5_click_download(self, game_name):
        """
        h5页面点击下载按钮
        Args:
            game_name: 游戏名
        Returns:
            True: 进入成功
            False：进入失败
         """
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=10)
        except:
            return False
        # try:
            # print(self.device.driver.contexts)
            # self.device.driver.switch_to.context("WEBVIEW_stetho_com.qiyi.video:plugin1")
            #self.device.find_element_by_xpath("//download-btn download countBtn[@data-desc='立即下载按钮']", timeout=5).click()
        #     time.sleep(2)
        #     self.device.tap([(540,1520)])
        #     self.device.tap([(540,1520)])
        #     time.sleep(5)
        #     self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
        #
        #     size = self.device.get_window_size()
        #     width = size.get('width')
        #     height = size.get('height')
        #     for i in range(50):
        #         try:
        #             self.device.find_element_by_xpath("//android.widget.Button[@text='官方推荐']", timeout=5)
        #             break
        #         except:
        #             if i == 49:
        #                 g_logger.error("下载超时")
        #                 return False
        #             time.sleep(5)
        #             continue
        #     time.sleep(1)
        #     self.device.click_by_id(self.conf.gamecenter_game_download_cancel.id, timeout=5, desc="点击取消按钮")
        # except Exception as e:
        #     return False
        return True

    def delete_game(self):
        """
        删除管理器中未安装的游戏
        Returns:
            True: 进入成功
            False：进入失败
         """
        try:
            time.sleep(2)
            self.device.click_by_id("com.qiyi.gamecenter:id/down_load", timeout=5, desc="点击下载管理器按钮")
            time.sleep(2)
            self.device.click_by_id("com.qiyi.gamecenter:id/iv_download_delete", timeout=5, desc="点击删除按钮")
            time.sleep(2)
            self.device.click_by_id("com.qiyi.gamecenter:id/cancel", timeout=5, desc="点击弹框中确认删除按钮")
        except Exception as e:
            return False
        return True