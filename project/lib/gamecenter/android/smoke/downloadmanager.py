# -*- coding: UTF-8 -*-

"""
File Name:      downloadmanager
Author:         zhangwei04
Create Date:    2018/11/20
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.gamecenter.android.smoke.common import Common


class DownloadManager(Common):
    """下载管理器页面"""
    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def check_ui(self):
        """
        检测下载管理器UI界面
        Returns:
            True: 检测成功， False: 检测失败
        """
        try:
            time.sleep(5)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='更新']", timeout=10)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='下载']", timeout=5)
            return True
        except Exception as e:
            g_logger.error("下载管理器检测UI失败")
            return False

    def check_download_tab(self):
        """
        检测下载标签UI
        Returns:
            True: 检测成功， False: 检测失败
        """
        try:
            dl_num = self.get_download_number()
            if dl_num is None:
                return False
            g_logger.info("下载tab游戏数量：{}".format(dl_num))
            if dl_num == 0:
                ele = self.device.swipe_ele_find_ele(find_xpath="//android.widget.TextView[@text='新游戏那么多，快去下载吧']",
                                                     swipe_id="com.qiyi.gamecenter:id/v_empty_games", direction='up', timeout=15)
                if not ele:
                    g_logger.error("查找游戏数量是0时，提示失败")
                    return False
            else:
                try:
                    self.device.find_element_by_xpath("//android.widget.TextView[contains(@text,'下载中')]", timeout=5)
                except:
                    self.device.find_element_by_xpath("//android.widget.TextView[contains(@text,'待安装')]", timeout=5)
        except Exception as e:
            g_logger.error("下载Tab检测失败")
            return False
        return True

    def check_update_tab(self):
        """
        检测更新标签UI
        Returns:
            True: 检测成功， False: 检测失败
        """
        try:
            update_ele = self.device.find_element_by_xpath(self.conf.download_manager_update.xpath_num, timeout=30)
            update_ele.click()
            time.sleep(3)
            update_num = int(update_ele.get_attribute("text"))
            g_logger.info("更新tab游戏数量：{}".format(update_num))
            if update_num == 0:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏都是最新的，赶紧去玩吧']", timeout=10)
            else:
                eles = self.device.find_elements_by_id("com.qiyi.gamecenter:id/vertical_game_item_name", timeout=5)
                game_name_list = [ele.get_attribute("text") for ele in eles]
                g_logger.info("更新游戏列表：{}".format(", ".join(game_name_list)))
        except Exception as e:
            return False
        return True

    def check_change(self):
        if not self.device.check_textview_text("为您精选", swipe=True, timeout=30):
            g_logger.warning("未找到为您精选模块")
            return False
        game_name = self.get_choiceness_first_game()
        if not game_name:
            return False

        self.click_change()
        time.sleep(3)
        change_game_name = self.get_choiceness_first_game()
        g_logger.info("下载管理器-为您精选第一款游戏名对比：{}, {}".format(game_name, change_game_name))
        if change_game_name:
            return game_name != change_game_name
        return False

    def get_update_number(self):
        """
        获取更新游戏数量
        Returns:
            dl_num：更新游戏数量 None: 获取失败
        """
        try:
            dl_num = int(self.device.find_element_by_xpath(self.conf.download_manager_update.xpath_num, timeout=30).get_attribute("text"))
            return dl_num
        except:
            g_logger.warning("获取更新数量失败")
            return None

    def get_download_number(self):
        """
        获取下载游戏数量
        Returns:
            dl_num：下载游戏数量 None: 获取失败
        """
        try:
            dl_num = int(self.device.find_element_by_xpath(self.conf.download_manager_download.xpath_num, timeout=30).get_attribute("text"))
            return dl_num
        except:
            g_logger.warning("获取更新数量失败")
            return None

    def get_choiceness_first_game(self):
        """
        获取为您精选页第一款游戏名
        Returns:
            成功：游戏名，失败：None
        """
        try:
            ele = self.device.find_element_by_xpath(self.conf.download_manager_choiceness.xpath_first_game, timeout=10)
        except:
            g_logger.error("获取为您精选第一款游戏名失败")
            return None
        return ele.get_attribute("text")

    def click_change(self):
        """
        点击换一批
        Returns:
            True: 找到换一批文本，并执行点击操作，False：没找到换一批文本
        """
        try:
            self.device.click_by_xpath(self.conf.download_manager_change.xpath, timeout=10)
            time.sleep(2)
            return True
        except:
            return False

    def update_game(self, game_name=None):
        """
        更新游戏
        Args:
            game_name: 更新游戏名，若不传入参数，则默认更新第一个游戏
        Returns:
        """
        # 切换至更新tab
        if not self.device.click_textview_text("更新", timeout=10):
            g_logger.error("点击更新Tab失败")
            return False
        update_number = self.get_update_number()
        if update_number is None:
            return False
        elif update_number == 0:
            g_logger.info("更新数量为0，未有游戏需要更新")
            return True
        else:
            if game_name:
                update_xpath = "//android.widget.TextView[@text='{}']//android.widget.ProgressBar[@resource-id='com.qiyi.gamecenter:id/pb_gamebutton']".format(game_name)
                try:
                    self.device.click_by_xpath(update_xpath, timeout=5)
                except:
                    g_logger.error("查找更新游戏按钮：{}失败".format(game_name))
                    return False
            else:
                try:
                    self.device.click_by_id("com.qiyi.gamecenter:id/vertical_game_item_download_btn", timeout=5)
                except:
                    g_logger.error("查找第一个更新游戏失败")
                    return False

            return self.game_install(game_name)

    def rm_will_install_app(self, app_name, timeout=20):
        """
        从待安装移除app
        Args:
            app_name: app名称
            timeout: 查找超时
        Returns:
            True: 移除成功, False: 移除失败
        """
        num = self.get_download_number()
        if not num:
            g_logger.info("下载数量为0")
            return True
        rm_xpath = self.conf.download_manager_to_install.xpath_rm.format(app_name)
        ele = self.device.swipe_down_find_ele(xpath=rm_xpath, timeout=timeout)
        if ele:
            ele.click()
            time.sleep(2)
        else:
            g_logger.error("下载管理器，未找到待移除的游戏：{}".format(app_name))
            return False
        try:
            self.device.click_by_xpath(self.conf.common_button.xpath.format("删除"), timeout=10)
            time.sleep(3)
        except:
            pass
        return True



