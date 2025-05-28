# -*- coding: UTF-8 -*-

"""
File Name:      roomplayer
Author:         zhangwei04
Create Date:    2019/8/9
"""

import os
import time
import re
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.glive.pc.common import Common
from framework.utils.selenium.action_chains import ActionChains
import contextlib


class RoomPlayer(Common):
    """直播间播控"""
    def __init__(self, target, ele_conf_name='pc'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def view_control(self):
        """
        显示底部控件
        Returns:
            True: 显示成功， False: 查找控件失败
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_player_control.right, timeout=3)
        if not ele:
            return g_logger.error("查找播控底部控制元素失败")
        ele.location_once_scrolled_into_view
        return True

    def pause(self):
        """
        暂停直播
        Returns:
        True: 暂停成功, False: 暂停失败
        """
        return self.device.click_by_xpath(self.conf.room_player_control.left_pause, desc="暂停按钮", timeout=3)

    def play(self):
        """
        播放直播
        Returns:
        True: 暂停成功, False: 暂停失败
        """
        return self.device.click_by_xpath(self.conf.room_player_control.left_play, time_sleep=1, desc="播放按钮", timeout=3)

    def check_pause(self):
        """
        检测暂停提示
        Returns:
            True: 检测成功, False: 检测失败
        """
        for i in range(20):
            if self.device.check_ele_text_by_xpath(self.conf.room_player_control.msg_tip, text="暂停", timeout=0.2):
                return g_logger.info("检测到暂停tips")
        else:
            return g_logger.error("检测暂停tips超时")

    def check_play(self):
        """
        检测暂停提示
        Returns:
            True: 检测成功, False: 检测失败
        """
        for i in range(20):
            if self.device.check_ele_text_by_xpath(self.conf.room_player_control.msg_tip, text="播放", timeout=0.2):
                return g_logger.info("检测到暂停tips")
        else:
            return g_logger.error("检测暂停tips超时")

    def full_screen(self):
        """
        全屏播放
        Returns:
            True: 全屏播放， False: 查找全屏按钮失败
        """
        conf = self.conf.room_player_control
        return self._click_ele_check_ele(conf.right_full_screen, conf.right_exit_full_screen, "全屏按钮", "退出全屏按钮")

    def exit_full_screen(self):
        """
        退出全屏
        Returns:

        """
        conf = self.conf.room_player_control
        return self._click_ele_check_ele(conf.right_exit_full_screen, conf.right_full_screen, "退出全屏按钮", "全屏按钮")

    def full_page(self):
        """
        页面全屏播放
        Returns:
        """
        conf = self.conf.room_player_control
        return self._click_ele_check_ele(conf.right_full_page, conf.right_exit_full_page, "网页全屏按钮", "退出网页全屏按钮")

    def exit_full_page(self):
        """
        页面全屏播放
        Returns:
        """
        conf = self.conf.room_player_control
        ret = self._click_ele_check_ele(conf.right_exit_full_page, conf.right_full_page, "退出网页全屏按钮", "网页全屏按钮")
        time.sleep(0.5)
        h2_ele = self.device.get_ele_by_tag_name("h2")
        if h2_ele:
            self.device.move_to_element(h2_ele)
        else:
            return g_logger.error("查找H2 tag名失败")
        time.sleep(0.5)
        return ret

    def _click_ele_check_ele(self, click_xpath, check_xpath, click_desc="", check_desc=""):
        """
        点击元素，检测元素
        Args:
            click_xpath: 点击元素，全屏、退出全屏、网页全屏、网页退出全屏xpath路径
            check_xpath: 检测元素，退出全屏、全屏、网页退出全屏、网页全屏xpath路径
            click_desc: 点击描述
            check_desc: 检测描述
        Returns:
            True: 执行成功, False: 执行失败
        """
        conf = self.conf.room_player_control
        size1 = self.device.get_ele_by_xpath(conf.xpath).size
        g_logger.info("原播控size: {}".format(size1))
        self.view_control()
        if not self.device.click_by_xpath(click_xpath, desc=click_desc, time_sleep=2):
            return False

        size2 = self.device.get_ele_by_xpath(conf.xpath).size
        g_logger.info("全屏后播控size: {}".format(size2))
        ele_exit = self.device.get_ele_by_xpath(check_xpath)
        if ele_exit:
            return True
        else:
            return g_logger.error("查找{}失败".format(check_desc))

    def reload(self):
        """
        刷新直播间
        Returns:
        True: 刷新成功, False: 刷新失败
        """
        conf = self.conf.room_player_control
        control_tip_ele = self.device.get_ele_by_xpath(conf.control_tip, timeout=2)
        if not control_tip_ele:
            return g_logger.error("查找正在加载提示元素失败")
        if not self.device.click_by_xpath(conf.left_reload, time_sleep=0.5, desc="刷新按钮"):
            return False
        time_start = time.time()
        while 5 > time.time() - time_start:
            if control_tip_ele.is_displayed():
                g_logger.info("加载提示: {}".format(control_tip_ele.text))
                time.sleep(2)
                break
            time.sleep(0.1)
        else:
            return g_logger.error("查找显示稍候加载提示超时")

        return True

    def click_danmu(self):
        """
        关闭弹幕
        Returns:
            True: 关闭成功, False: 关闭失败
        """
        self.view_control()
        time.sleep(0.5)
        if not self.device.click_by_xpath(self.conf.room_player_control.right_danmu, desct='弹幕', timeout=3):
            return False
        return True

    def check_danmu_closed(self):
        """
        检测弹幕是否关闭
        Returns:
            True:弹幕关闭， False:弹幕未关闭
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_player_control.right_danmu, timeout=3)
        if not ele:
            return g_logger.error("获取弹幕按钮元素失败")
        damnu_cls = ele.get_attribute("class")
        return "danmuOff" in damnu_cls

    def check_danmu_opened(self):
        ele = self.device.get_ele_by_xpath(self.conf.room_player_control.right_danmu, timeout=3)
        if not ele:
            return g_logger.error("获取弹幕按钮元素失败")
        damnu_cls = ele.get_attribute("class")
        return "danmuOff" not in damnu_cls

    def _get_voice_height_top_px(self):
        """
        读取音量按钮距离顶部和底部像素
        Returns:
            height: 高度
            top: 长度
        """
        conf = self.conf.room_player_control
        ele = self.device.get_ele_by_xpath(conf.right_voice)
        if not ele:
            return g_logger.error("查找音量元素失败"), None
        try:
            line_ele = ele.find_element_by_xpath(conf.voice_bg_line)
            style = line_ele.get_attribute("style")
            height, top = re.findall("(\d+)", style)
            return int(height), int(top)
        except:
            return g_logger.error("查找像素失败"), None

    def _get_voice_percent(self):
        """
        读取音量显示百分比
        Returns:
            int: 百分比数值
        """
        conf = self.conf.room_player_control
        ele = self.device.get_ele_by_xpath(conf.right_voice)
        if not ele:
            return g_logger.error("查找音量元素失败"), None
        try:
            percent_ele = ele.find_element_by_xpath(conf.voice_bg_percent)
            voice_per = int(percent_ele.text[:-1])
            g_logger.info("当前音量百分比值：{}".format(voice_per))
            return voice_per
        except:
            return g_logger.error("读取音量百分比值失败")

    def voice_swipe(self, percent):
        """
        滑动影响
        Args:
            percent: 滑动到百分比的数量,如50
        Returns:
            True: 滑动成功, False: 滑动失败
        """
        if not self.view_control():
            return False
        if not self._show_voice_bg():
            return False
        percent = int(percent)
        cur_per = self._get_voice_percent()
        swipe_percent = percent - cur_per
        if swipe_percent:
            height, top = self._get_voice_height_top_px()
            swipe_px = - (height + top) * (float(swipe_percent) / 100)     # 需要取相反值，正数是往下滑
            return self.device.swipe_ele_by_xpath(self.conf.room_player_control.voice_bg_scroll_btn, height=swipe_px)

        else:
            return g_logger.info("当前处于{}%，不进行滑动".format(cur_per))

    def _show_voice_bg(self):
        voice_icon = self.device.get_ele_by_xpath(self.conf.room_player_control.right_voice_icon)
        if voice_icon:
            self.device.move_to_element(voice_icon)
            return True
        else:
            return g_logger.error("查找音量按钮元素失败")

    def check_voice_percent(self, percent):
        """
        检测当前音量百分比
        Args:
            percent: 检测值
        Returns:
            True: 检测成功, False: 检测失败
        """
        if not self.view_control():
            return False
        if not self._show_voice_bg():
            return False
        return abs(int(percent) - self._get_voice_percent()) < 5

    def click_video_start_button(self, timeout=6):
        """
        点击'点击播放'按钮,播放视频
        Returns:
            True: 点击成功, False: 点击失败
        """
        play_button_img = os.path.join(self.conf_img_dir, "video_start.png")
        video_screen_img = os.path.join(g_resource['testcase_log_dir'], "video_screen.png")
        time_start = time.perf_counter()
        while timeout > time.perf_counter() - time_start:
            ele = self.device.get_ele_by_id(self.conf.room_player.id, timeout=1)
            if not ele:
                return g_logger.error("查找video失败")
            ele.screenshot(video_screen_img)
            result = self.match_image(video_screen_img, play_button_img, confidence=0.9)
            if result:
                self.device.tap(result['result'], time_sleep=3)
                return True

    def check_video_start(self, timeout=10):
        """
        检测video播放
        Returns:
            True: 视频播放， False: 视频未播放
        """
        danmu_66666_img = os.path.join(self.conf_img_dir, "66666.png")
        video_screen_img = os.path.join(g_resource['testcase_log_dir'], "video_screen.png")
        if not self.target.LiveRoom.chat_send_msg("66666", time_sleep=2):
            return g_logger.error("发送66666失败")
        time_start = time.time()
        while timeout > time.time() - time_start:
            ele = self.device.get_ele_by_id(self.conf.room_player.id, timeout=1)
            if not ele:
                return g_logger.error("查找video失败")
            ele.screenshot(video_screen_img)
            result = self.match_image(video_screen_img, danmu_66666_img, confidence=0.5)
            if result:
                g_logger.info(result, console=False)
                return True
            time.sleep(1)
        else:
            return g_logger.error("检测弹幕66666超时")


