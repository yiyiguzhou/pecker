# -*- coding: UTF-8 -*-

"""
File Name:      gamepage
Author:         zhangwei04
Create Date:    2019/1/7
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from framework.utils.threads import IpeckerThread
from project.lib.gamecenter.android.smoke.common import Common


class GamePage(Common):
    """游戏页"""
    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
        self.screen_path = os.path.join(g_resource['testcase_log_dir'], "h5_game_exit_dl_toast_screen.png")

    def click_native_exit_picture(self):
        """
        点击Native游戏退出图片
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            self.device.click_by_id(self.conf.native_game_exit.id_pic, desc="点击Native游戏退出图片", timeout=20)
            time.sleep(5)
            return True
        except:
            return False

    def click_native_exit_more_game(self):
        """
        点击Native游戏退出更多游戏
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            self.device.click_by_xpath(self.conf.native_game_exit.xpath_more_game, desc="点击Native游戏退出更多游戏", timeout=20)
            time.sleep(5)
            return True
        except:
            return False

    def click_native_exit(self):
        """
        点击Native游戏退出更多游戏
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            self.device.click_by_xpath(self.conf.native_game_exit.xpath_exit, desc="点击Native游戏退出按钮", timeout=20)
            time.sleep(3)
            return True
        except:
            return False

    def check_native_exit_ui(self, timeout=10):
        """
        检测Native游戏退出界面UI, 根据是否有退出游戏的按钮确认是否处于游戏退出页面
        Args:
            timeout: 检测超时
        Returns:
            True: 检测成功, False: 检测失败i
        """
        try:
            self.device.find_element_by_xpath(self.conf.native_game_exit.xpath_exit, timeout=timeout)
            return True
        except:
            return False

    def into_exiting_native_game(self, timeout=30):
        """
        进入退出Native游戏界面
        Args:
            timeout: 超时
        Returns:
            True: 进入成功, False: 进入失败
        """
        time_start = time.time()
        while timeout > time.time() - time_start:
            self.device.adb.adb_shell('input keyevent KEYCODE_BACK')
            time.sleep(3)
            if self.check_native_exit_ui(timeout=5):
                return True
            else:
                try:
                    self.device.click_by_xpath("//android.widget.TextView[@text='一键授权登录']", timeout=5)
                    time.sleep(3)
                except:
                    pass
        else:
            return False

    def check_h5_exit_ui(self, timeout=10):
        """
        检测Native游戏退出界面UI, 根据是否有退出游戏的按钮确认是否处于游戏退出页面
        Args:
            timeout: 检测超时
        Returns:
            True: 检测成功, False: 检测失败i
        """
        try:
            self.device.find_element_by_xpath(self.conf.h5_game_exit.xpath_exit, timeout=timeout)
            return True
        except:
            return False

    def into_exiting_h5_game(self, timeout=120):
        """
        进入退出H5游戏界面
        Args:
            timeout: 超时
        Returns:
            True: 进入成功, False: 进入失败
        """
        time_start = time.time()
        while timeout > time.time() - time_start:
            self.device.adb.adb_shell('input keyevent KEYCODE_BACK')
            time.sleep(3)
            if self.check_h5_exit_ui(timeout=5):
                return True
            else:
                try:
                    self.device.click_by_xpath("//android.widget.TextView[@text='一键授权登录']", timeout=5)
                    time.sleep(3)
                except:
                    pass
        else:
            return False

    def click_h5_exit(self):
        """
        点击H5游戏退出游戏
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            self.device.click_by_xpath(self.conf.h5_game_exit.xpath_exit, desc="点击H5游戏退出游戏按钮", timeout=10)
            time.sleep(3)
            return True
        except:
            return False

    def click_h5_exit_more_game(self):
        """
        点击H5游戏退出更多游戏
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            self.device.click_by_xpath(self.conf.h5_game_exit.xpath_more_game, desc="点击H5游戏退出更多游戏", timeout=20)
            time.sleep(5)
            return True
        except:
            return False

    def click_h5_exit_download_wd(self):
        """
        点击H5游戏退出页面下载微端
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            self.device.click_by_id(self.conf.h5_game_exit.id_download_wd, desc="点击下载微端", timeout=10)
            time.sleep(0.2)
            self.device.get_screenshot_as_file(self.screen_path)
            return True
        except:
            return False

    def click_h5_exit_recommend_game(self, game_name):
        """
        点击H5游戏退出页面推荐游戏名
        Args:
            game_name: 游戏名
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            self.device.click_by_xpath(self.conf.h5_game_exit.xpath_recommend_game.format(game_name), desc='点击H5游戏退出界面推荐游戏列表游戏', timeout=5)
            time.sleep(2)
            return True
        except:
            return False

    def click_check_h5_exit_first_game(self):
        """
        点击H5游戏退出页面第一个游戏,并检测是否进入成功
        Args:
            game_name: 游戏名
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            ele = self.device.find_element_by_xpath(self.conf.h5_game_exit.xpath_first_game_name, timeout=10)
            game_name = ele.get_attribute("name")
        except Exception as e:
            g_logger.error("查找第一款游戏名失败")
            return False

        try:
            self.device.click_by_xpath(self.conf.h5_game_exit.xpath_recommend_game.format(game_name), desc='点击推荐游戏{}'.format(game_name), timeout=5)
            time.sleep(5)
        except:
            g_logger.error("点击第一款游戏{}失败".format(game_name))
            return False

        return self.check_h5_game(game_name)

    def check_app_installing_page(self):
        """
        检测是否是app安装界面
        Returns:
            True: 处于app安装界面, False: 不处于app安装界面
        """
        manufact = self.device.get_manufacturer()
        ui_version = self.device.get_ui_version()
        if manufact == "huawei":
            if ui_version > "8.0":
                if self.device.check_textview_text("是否允许“爱奇艺”安装应用？", timeout=10):
                    return True
                else:
                    return False
            else:
                try:
                    self.device.find_element_by_id("com.android.packageinstaller:id/decide_to_continue", timeout=10)
                    return True
                except:
                    return False
        elif manufact == "xiaomi":
            pass  # 待补充

    def check_h5_exit_download_app_toast(self):
        """
        检测H5游戏退出页面，已下载app后，点击下载微端后的toast提示
        Returns:
            True: 检测成功, False: 检测失败
        """
        des_png_path = os.path.join(self.conf_img_dir, "h5_game_exit_dl_toast.png")
        result = self.match_image(self.screen_path, des_png_path, confidence=0.8)
        return True if result else False

    def cancel_install_app(self):
        """
        app安装页面取消app安装
        Returns:
            True: 取消成功, False: 取消失败
        """
        if not self.check_app_installing_page():
            g_logger.warning("检测处于app安装页面失败")
            return False
        manufacturer = self.device.get_manufacturer()
        if manufacturer == "huawei":
            self.device.adb.adb_shell('input keyevent KEYCODE_BACK')
            time.sleep(2)
            return True
        elif manufacturer == "huawei":
            pass  # 待添加处理流程

    def back_to_h5_exit_page(self, timeout=120):
        """
        回退到游戏退出界面
        Args:
            timeout: 检测超时
        Returns:
            True: 回退成功, False: 回退失败
        """
        return self.cmd_back_and_find_ele(xpath=self.conf.h5_game_exit.xpath_exit, timeout=timeout)

    def check_h5_game(self, game_name):
        """
        检测H5游戏，当前是否运行此h5游戏
        Args:
            game_name: 游戏名
        Returns:
            True: 检测成功, False: 检测失败
        """
        game_xpath = "//android.view.View[@resource-id='game_url']/android.view.View[@content-desc='{}']".format(game_name)
        g_logger.info("检测H5游戏：{}".format(game_name))
        try:
            self.device.find_element_by_xpath(game_xpath, timeout=15)
            return True
        except:
            g_logger.warning("检测当前H5游戏：{}失败".format(game_name))
            return False

