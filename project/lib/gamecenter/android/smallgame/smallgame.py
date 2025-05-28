# -*- coding: UTF-8 -*-

"""
File Name:      demo
Author:         zhangwei04
Create Date:    2018/1/9
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android


class SmallGame(Android):
    def __init__(self, target):
        super().__init__(target=target)

        self.target = target
        self.data = target.data
        self.device = target.device

    def into_desktop_small_game_app(self):
        self.device.adb.adb_shell("am force-stop com.qiyi.video")
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')
        for i in range(2):
            self.device.adb.adb_shell("input keyevent 3")
            time.sleep(0.5)
        for i in range(5):
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺小游戏']", timeout=5).click()
                time.sleep(5)
                return True
            except:
                if i == 4:
                    return False
                self.device.swipe(width * 2 / 3, height * 1 / 2, width * 1 / 3, height * 1 / 2)
                time.sleep(1)
        return True

    def into_h5_game_from_samll_game_app(self, game_name):
        """
        从小游戏中心进入游戏
        Returns:
            True：进入成功
            False：进入失败
        """
        for i in range(5):
            try:
                time.sleep(2)
                g_logger.info("点击进入小游戏...")
                self.device.find_element_by_xpath('//android.view.View[@text="{}"]'.format(game_name), timeout=5).click()
                g_logger.info("点击进入小游戏成功")
                time.sleep(10)
                return True
            except:
                continue
        return False

    def out_game_from_sider(self):
        """
        从侧边栏退出小游戏
        Returns:
            True：进入成功
            False：进入失败
        """
        try:
            for i in range(3):
                try:
                    time.sleep(2)
                    g_logger.info("点击侧边栏...")
                    self.device.find_element_by_id('javascript:;', timeout=2).click()
                    g_logger.info("点击侧边栏成功")
                    time.sleep(0.2)
                    g_logger.info("点击侧边栏退出...")
                    self.device.find_element_by_id('quit', timeout=5).click()
                    g_logger.info("点击侧边栏退出成功")
                    time.sleep(2)
                    break
                except:
                    if i == 2:
                        g_logger.warning("查找侧边栏失败，命令行调起退出")
                        # self.into_small_game_app()
                        self.device.adb.adb_shell("input keyevent 4")
                        time.sleep(1)

            g_logger.info("点击立即退出...")
            self.device.find_element_by_id('xyx_exit_game_sure', timeout=5).click()
            g_logger.info("点击立即退出成功")
            time.sleep(10)
        except Exception as e:
            return False
        return True

    def base_into_small_game(self):
        """
        从基线进入小游戏
        Returns:
            True：进入成功
            False：进入失败
        """
        time.sleep(5)
        try:
            # self.device.click_by_id(self.conf.base_recommend.id, timeout=5)
            self.device.click_textview_text("首页", timeout=5)
            time.sleep(3)
            self.device.find_element_by_xpath(self.conf.base_recommend_gamecenter.xpath, timeout=5)  # 找到游戏中心
            try:
                self.device.find_element_by_xpath(self.conf.base_recommand_small_game.xpath, timeout=5)
            except:
                # 展开
                pass
        except:
            pass