# -*- coding: UTF-8 -*-

"""
File Name:      base
Author:         zhangwei04
Create Date:    2018/12/18
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from framework.utils.threads import IpeckerThread
from project.lib.gamecenter.android.smoke.common import Common


class BasePage(Common):
    """基线页面"""

    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def into_my(self):
        """
        进入'我的'页面
        Returns:
            True: 进入, False:未找到我的
        """
        for i in range(2):
            ele = self._stable_element(xpath="//android.widget.TextView[@text='我的']", timeout=30)
            if ele:
                ele.click()
                time.sleep(3)
                g_logger.info("点击基线'我的'成功")
                windwos_size = self.device.get_window_size()
                w, h = windwos_size['width'], windwos_size['height']
                g_logger.info("向下滑动一些屏幕，防止卡死")
                self.device.adb.adb_shell("input swipe {} {} {} {}".format(w/2, h/3, w/2, h/2))
                time.sleep(2)
                break
            else:
                try:
                    g_logger.info("查看并点击升级弹窗")
                    self.device.click_by_xpath(self.conf.base_upgrade_close.xpath, timeout=5, desc="点击暂不升级按钮")
                    time.sleep(1)
                    continue
                except:
                    pass
        else:
            g_logger.error("查找基线'我的'入口失败")
            return False

        return True

    def into_home_page(self):
        """
        进入基线home页
        Returns:
            True：进入成功，False: 进入失败
        """
        for i in range(3):
            try:
                self.device.click_by_id(self.conf.base_recommend.id, timeout=5, desc="点击基线推荐tab")
                time.sleep(3)
                self.device.find_element_by_xpath(self.conf.base_recommend_gamecenter.xpath, timeout=10)
                return True
            except:
                if self.device.click_textview_text("同意并继续", timeout=3):
                    time.sleep(2)
                    continue
                try:
                    self.device.click_by_xpath(self.conf.base_upgrade_close.xpath, timeout=5, desc="点击暂不升级按钮")
                    time.sleep(1)
                    continue
                except:
                    pass
        else:
            g_logger.info("进入基线首页失败")
            return False

    def my_into_gc(self):
        """
        基线我的页面点击我的游戏，进入游戏中心首页
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_textview_text("我的游戏", swipe=True, timeout=120)

    def into_task_center(self):
        """
        进入任务中心
        Returns:
        """
        try:
            self.device.click_textview_text("做任务领积分", timeout=20)
            time.sleep(3)
        except:
            g_logger.error("查找做任务领积分失败")
            return False
        # 点掉连续签到弹框
        if self.device.check_textview_text("连续签到可获得更多积分", timeout=10) or self.device.check_textview_text("签到成功", timeout=5):
            try:
                self.device.click_by_xpath("//android.view.ViewGroup[last()]/android.widget.ImageView", timeout=5)
                time.sleep(2)
            except:
                pass
        for i in range(2):
            if self.device.check_textview_text("任务中心", timeout=5):
                return True
            else:
                g_logger.info("任务中心可能有全屏弹窗，截图保存至check_full_sacreen.png并使用back建点掉")
                self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "check_full_screen.png"))
                self.key_event("KEYCODE_BACK")
                self.device.swipe_screen(rate=0.3, direction='down')  # 需要滑动刷新下界面，否则无法获取到
        else:
            g_logger.error("检测任务中心标题:任务中心失败")
            return False

    def task_center_into_list(self):
        """
        任务中心进入任务列表
        Returns:
            True: 点击任务列表成功， False: 查找任务列表入口失败
        """
        task_list_xpath = "//android.widget.TextView[contains(@text, '今日还可赚') and contains(@text, '积分')]"
        ele = self.device.swipe_down_find_ele(xpath=task_list_xpath)
        if ele:
            ele.click()
            time.sleep(3)
            return True
        else:
            g_logger.error("点击今日还可赚***积分进入任务列表失败")
            return False

    def back_to_task_list(self):
        for i in range(5):
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            if self.device.check_textview_text("任务列表", timeout=5):
                return True
        return False

    def back_to_task_center(self):
        for i in range(5):
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(2)
            if self.device.check_textview_text("任务中心", timeout=5):
                return True
        return False

    def check_task_list_start_game_status(self, status="去完成"):
        """
        检测任务列表启动游戏状态
        Args:
            status: 任务状态：去完成、领取、已完成、去观看、去分享、去评分
        Returns:
            True: 状态匹配成功, False: 状态匹配失败
        """
        if not self.device.check_textview_text("启动游戏", swipe=True, timeout=60):
            g_logger.warning("查找启动游戏文本失败")
            return False
        xpath_module = "//android.widget.TextView[@text='启动游戏']/..//android.widget.TextView[@text='{}']".format(status)
        try:
            self.device.find_element_by_xpath(xpath_module.format(status), timeout=5)
            g_logger.warning("检查任务完成状态失败")
            return True
        except:
            return False

    def doing_start_game_task_list(self, game_name=None):
        """
        开始启动游戏任务
        Args:
            game_name: 游戏名
        Returns:
        """
        task_name = '启动游戏'
        if self.check_task_list_start_game_status("去完成"):
            # 完成流程
            try:
                self.device.click_by_xpath("//android.widget.TextView[@text='{}']/..//android.widget.TextView[@text='去完成']".format(task_name))
                time.sleep(5)
            except:
                g_logger.error("查找'去完成失败'")
                return False
            g_logger.info("搜索游戏进入游戏详情")
            self.target.HomePage.game_search_click_icon(game_name)
            g_logger.info("打开游戏")
            self.target.GameDetailPage.game_detail_download()
            time.sleep(5)
            g_logger.info("关闭游戏")
            self.device.adb.stop_app(self.app_conf.get(game_name, "package"))
            g_logger.info("back会到游戏列表页")
            if not self.back_to_task_center():
                return False
            g_logger.info("任务中心进入任务列表")
            if not self.task_center_into_list():
                return False
            g_logger.info("领取任务")
            if not self.get_task_integration(task_name):
                return False

        elif self.check_task_list_start_game_status("已完成"):
            g_logger.info("任务已经完成")
            return True
        elif self.check_task_list_start_game_status("领取"):
            g_logger.info("领取任务")
            return self.get_task_integration(task_name)

    def get_task_integration(self, task_name):
        """
        领取任务积分
        Args:
            task_name: 任务名称: 如启动游戏

        Returns:
            True: 领取任务积分成功， False: 获取失败
        """
        ele = self.device.swipe_down_find_ele(xpath="//android.widget.TextView[@text='{}']/..//android.widget.TextView[@text='领取']".format(task_name))
        if ele:
            ele.click()
            time.sleep(5)
        else:
            g_logger.info("领取任务积分：查找任务领取按钮失败")
            return False
        # ele = self.device.swipe_down_find_ele(xpath="//android.widget.TextView[@text='{}']/..//android.widget.TextView[@text='已完成']".format(task_name))
        return self.check_task_list_start_game_status("已完成")

    def into_ask(self):
        """
        进入导航页
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            self.device.click_by_id(self.conf.base_ask.id, desc="点击导航图标", timeout=15)
            time.sleep(3)
            return True
        except:
            return False

    def ask_into_gc(self):
        """
        导航页进入游戏中心
        Returns:
            True: 点击任务中心成功, False: 点击任务中心失败
        """
        return self.device.click_textview_text("游戏中心", swipe=True, timeout=120)

    def click_home_search_button(self):
        """
        点击首页搜索按钮，进入搜索页
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            self.device.click_by_id("com.qiyi.video:id/right_search_icon", desc="点击基线首页搜索按钮进入搜索页", timeout=15)
            time.sleep(2)
            return True
        except:
            return False

    def search_page_search_text(self, text):
        """
        搜索页搜索文本
        Args:
            text: 待搜索的文本
        Returns:
            True: 搜索成功, False: 搜索失败
        """
        try:
            self.device.find_element_by_xpath("//android.widget.EditText", timeout=15).set_text(text)
            return True
        except:
            return False

    def search_page_click_associate_text(self, text):
        """
        搜索页点击联想词
        Args:
            text: 联想词
        Returns:
            True: 点击成功, False: 点击失败
        """
        if self.device.click_textview_text(text, timeout=10):
            time.sleep(2)
            return True
        else:
            return False

    def video_detail_in_game_detail(self, game_name):
        """
        视频详情页进入游戏详情页
        Args:
            game_name: 游戏名
        Returns:
            True: 点击有心名成功, False
        """
        if not self.device.click_textview_text("游戏", timeout=10):
            g_logger.error("切换到游戏tab失败")
            return False

        game_xpath = "//android.support.v7.widget.RecyclerView[@resource-id='com.qiyi.video:id/recycler']//android.widget.TextView[@text='{}']".format(game_name)
        try:
            self.device.click_by_xpath(game_xpath, desc="视频详情页点击游戏{}".format(game_name), timeout=10)
            time.sleep(3)
            return True
        except:
            return False

    def video_detail_click_play(self):
        """
        视频详情页点击播放按钮，跳转至半屏播放页面
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_textview_text("继续播放") or self.device.click_textview_text("立即播放")

    def video_play_into_game(self, game_name):
        """
        视频播放页进入游戏
        Args:
            game_name: 游戏名
        Returns:
            True: 找到游戏并点击成功, False: 点击失败
        """
        swipe_xapth = self.conf.base_video_detail_play.xpath_ip_relate
        find_xpath = self.conf.base_video_detail_play.xpath_ip_relate_game.format(game_name)
        ele = self.device.swipe_ele_find_ele(find_xpath=find_xpath, swipe_xpath=swipe_xapth, direction="left", rate=0.2, timeout=120)
        if ele:
            ele.click()
            time.sleep(3)
            return True
        else:
            return False

    def click_bottom_home(self):
        """
        点击底部栏的首页
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_textview_text("首页", timeout=15)

