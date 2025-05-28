# -*- coding: UTF-8 -*-

"""
File Name:      MyInfoPage
Author:         zhangwei04
Create Date:    2018/12/11
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.gamecenter.android.smoke.common import Common
from appium.webdriver.common.touch_action import TouchAction

ENV_TYPES_DICT = {"online": "正式环境", "pre_release": "预发布环境", "test": "测试环境"}   # 环境字典


class ClassifyPage(Common):
    """个人中心页面"""

    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
        height = self.device.get_window_height()

        str_pre = "_2880" if height in (2880, 2712) else "_1280" if height in (1280,) else ""
        self.hot_pic = os.path.join(self.conf_img_dir, "classify_tab_hot{}.png".format(str_pre))
        self.lastest_pic = os.path.join(self.conf_img_dir, "classify_tab_lastest{}.png".format(str_pre))

    def check_ui(self, mark_tab='推荐'):
        """
        检测分类页UI
        Args:
            mark_tab: 选择的tab，即当前页面所展示的tab
        Returns:
            True: 检测成功, False: 检测失败
        """
        try:
            self.device.find_element_by_xpath(self.conf.classify.xpath_title, timeout=20)
        except Exception as e:
            g_logger.error("分类页查找标题失败")
            return False
        return self._check_tab_select(mark_tab)

    def _check_tab_select(self, tab_name):
        """
        检测tab是否被选择
        Args:
            tab_name: tab名称
        Returns:

        """
        try:
            ele = self.device.find_element_by_xpath(self.conf.classify.xpath_mark_tab, timeout=10)
            return tab_name == ele.get_attribute('text')
        except Exception as e:
            g_logger.error("分类页查找标记失败")
            return False

    def check_home_ui(self):
        """
        检测推荐页UI
        Args:
            title: 横排游戏标题
        Returns:
            True: 检测成功, False: 检测失败
        """
        if not self.check_ui("推荐"):
            return False

        eles = self.device.find_elements_by_xpath(self.conf.classify_home.xpath_big_pics, timeout=20)
        if not eles:
            g_logger.error("查找推荐页大图模块失败")
            return False

        return True

    def check_tab_ui(self, tab_name, game_name=None):
        """
        检测分类标签 UI，包含
        Args:
            tab_name: 分类标签
            game_name: 游戏名
        Returns:
            True: 检测成功, False: 检测失败
        """
        if not self._check_tab_select(tab_name):
            return False

        if not self._check_host_lastest_icon_view():
            g_logger.error("检测最新最热按钮图标失败")
            return False
        if game_name:
            if not self.check_tab_game(game_name):
                g_logger.error("检测游戏:{}失败".format(game_name))
                return False

        return True

    def check_tab_default_ui(self, tab_name, game_name=None):
        """
        Args:
            tab_name: 标签名
            game_name: 游戏名
        Returns:
            True: 检测成功, False: 检测失败
        """
        if not self._check_tab_select(tab_name):
            return False

        if not self.check_tab_in_hot_icon():
            g_logger.error("检测处于最热按钮图标失败")
            return False
        if game_name:
            if not self.check_tab_game(game_name, order=True):
                g_logger.error("检测游戏:{}失败".format(game_name))
                return False
        return True

    def check_tab_lastest_ui(self, tab_name, game_name=None):
        """
        检测最新标签页UI
        Args:
            tab_name: 标签名
            game_name: 游戏名
        Returns:
            True: 检测成功, False: 检测失败
        """
        if not self._check_tab_select(tab_name):
            return False

        if not self.check_tab_in_lastest_icon():
            g_logger.error("检测处于最热按钮图标失败")
            return False
        if game_name:
            if not self.check_tab_game(game_name, order=True):
                g_logger.error("检测游戏:{}失败".format(game_name))
                return False
        return True

    def click_tab(self, tab_name):
        """
        点击tab
        Args:
            tab_name: tab名
        Returns:
            True: 点击成功，False: 点击失败
        """
        ele = self.device.swipe_ele_find_ele(find_xpath=self.conf.classify.xpath_tab.format(tab_name), swipe_id=self.conf.classify.id_left, timeout=30)
        if ele:
            ele.click()
            time.sleep(5)
            return True
        else:
            g_logger.error("点击分类标签：{}失败".format(tab_name))
            return False

    def home_horizontal_look_all(self, horizon_title):
        """
        推荐页横排游戏查看全部游戏
        Args:
            horizon_title: 横排专题
        Returns:
            True: 进入查看全部游戏专题成功， False: 进入失败
        """
        find_xpath = self.conf.classify_home.xpath_horizon_look_all.format(horizon_title)
        ele = self.device.swipe_ele_find_ele(find_xpath=find_xpath, swipe_id=self.conf.classify.id_content, rate=0.4, timeout=120)
        if ele:
            ele.click()
            time.sleep(4)
        else:
            g_logger.error("未找到横排：{}的查看全部游戏".format(horizon_title))
            return False

        return self.check_topic_ui(horizon_title)

    def home_click_big_pic(self, pos):
        """
        推荐页点击大图
        Args:
            pos: 图片位置,从1开始
        Returns:
            True: 点击成功，False: 点击失败
        """
        eles = self.device.find_elements_by_xpath(self.conf.classify_home.xpath_big_pics, timeout=20)
        index = int(pos) - 1
        if eles and len(eles) >= index:
            ele = eles[index]
            ele.click()
            time.sleep(3)
            return True
        else:
            g_logger.warning("推荐页点击位置为{}的大图失败".format(pos))
            return False

    def home_click_game_icon(self, game_name):
        """
        推荐页天机游戏icon
        Args:
            game_name: 游戏名
        Returns:
            True: 点击图表成功, False: 点击失败
        """
        ele = self.device.swipe_down_find_ele(xpath=self.conf.classify_home.xpath_game_icon.format(game_name), timeout=180)
        if ele:
            ele.click()
            time.sleep(3)
            return True
        else:
            g_logger.error("查找游戏：{}失败".format(game_name))
            return False

    def tab_switch_hot_icon(self):
        """
        最新最热图标切换至最新高亮
        Returns:
            True: 切换成功, False: 切换失败
        """
        if self.check_tab_in_hot_icon():
            return True
        else:
            try:
                self.device.click_by_id(self.conf.classify_tab.id_switch_hot_lastest, desc="点击最热最新按钮，切换至最热", timeout=10)
                time.sleep(5)
                return self.check_tab_in_hot_icon(timeout=10)
            except:
                return False

    def tab_switch_lastest_icon(self):
        """
        最新最热图标切换至最新高亮
        Returns:
            True: 切换成功, False: 切换失败
        """
        if self.check_tab_in_lastest_icon():
            return True
        else:
            try:
                self.device.click_by_id(self.conf.classify_tab.id_switch_hot_lastest, desc="点击最热最新按钮，切换至最新", timeout=10)
                time.sleep(5)
                return self.check_tab_in_lastest_icon(timeout=10)
            except:
                return False

    def check_tab_in_hot_icon(self, timeout=5):
        """
        检测最新最热图标是否处于当前最热状态
        Args:
            timeout: 检测超时
        Returns:
            True: 检测成功, False: 检测失败
        """
        return self.match_any_image_to_screen(self.hot_pic, timeout=timeout)

    def check_tab_in_lastest_icon(self, timeout=5):
        """
        检测最新最热图标是否处于当前最新状态
        Args:
            timeout: 检测超时
        Returns:
            True: 检测成功, False: 检测失败
        """
        return self.match_any_image_to_screen(self.lastest_pic, timeout=timeout)

    def _check_host_lastest_icon_view(self, timeout=10):
        """
        检测最热最新图片是否显示出来
        Args:
            timeout: 检测超时
        Returns:
            True:检测成功， False: 检测失败
        """
        g_logger.info("检测最热最新图片是否显示出来")
        return self.match_any_image_to_screen((self.hot_pic, self.lastest_pic), timeout=timeout)

    def check_tab_game(self, game_name, order=False):
        """
        检测tab游戏名
        Args:
            game_name: 游戏名称
            order: 按照顺序检测
        Returns:
        """
        game_name_list = [game_name] if isinstance(game_name, str) else list(game_name)
        g_logger.info("检测游戏：{}".format(", ".join(game_name_list)))

        read_game_list = self._get_games_from_game(tuple(game_name_list), swipe_id=self.conf.classify.id_content)
        g_logger.info("读取到的游戏：{}".format(", ".join(read_game_list)))
        if read_game_list is None:
            return False
        if order:
            index_list = [read_game_list.index(game) if game in read_game_list else -1 for game in game_name_list]
            if index_list:
                return index_list == sorted(index_list)
            else:
                return False
        else:
            return game_name_list

    def check_game_list_page(self, title, game_name=None, order=False):
        """
        检测游戏列表页
        Args:
            title: 游戏列表页标题
            game_name: 游戏列表页检测游戏名，可以是列表
            order: 是否是有序排列
        Returns:
            True: 检测成功, False: 检测失败
        """
        try:
            self.device.find_element_by_xpath(self.conf.comment_title.xpath.format(title), timeout=20)
        except:
            g_logger.warning("检测标题：{}失败".format(title))
            return False

        # if game_name:
        #     game_name_list = [game_name] if isinstance(game_name, str) else list(game_name)
        #     g_logger.info("检测游戏：{}".format(", ".join(game_name_list)))
        #
        #     read_game_list = self._get_games_from_game(tuple(game_name_list))
        #     g_logger.info("读取到的游戏：{}".format(", ".join(read_game_list)))
        #     if read_game_list is None:
        #         return False
        #     if order:
        #         index_list = [read_game_list.index(game) if game in read_game_list else -1 for game in game_name_list]
        #         if index_list:
        #             return index_list == sorted(index_list)
        #         else:
        #             return False
        #     else:
        #         return game_name_list
        return True

    def _get_games_from_game(self, game_name_list, swipe_xpath=None, swipe_id=None, timeout=120):
        """
        读取分类tab的包含期望游戏页表的游戏
        Args:
            game_name_list: 期望游戏列表
            timeout: 超时
        Returns:
            list: 包含期望游戏里列表的游戏列表 None: 读取失败
        """
        game_name_list = [game_name_list] if isinstance(game_name_list, str) else list(game_name_list)
        time_start = time.time()
        found_game_list = []
        while timeout > time.time() - time_start:
            get_game_list = self._get_tab_games()
            if get_game_list is None:
                return None
            found_game_list.extend(get_game_list)
            inters_set = set(get_game_list).intersection(set(game_name_list))  # 交集
            if inters_set:
                for game_name in inters_set:
                    game_name_list.remove(game_name)
            if not game_name_list:
                break
            if swipe_xpath or swipe_id:
                self.device.swipe_ele(swipe_xpath=swipe_xpath, swipe_id=swipe_id, direction="up")
            else:
                self.device.swipe_screen(direction="up", sleep_time=3)
        return sorted(set(found_game_list), key=found_game_list.index)

    def _get_tab_games(self, tab_name=None, check_empty=True):
        """
        获取标签页游戏
        Args:
            tab_name: 标签页名字
            check_empty: 检测检测空页面
        Returns:
            list: 游戏列表 None:出现异常
        """
        if tab_name:
            try:
                self.device.click_by_xpath(self.conf.classify.xpath_tab.format(tab_name), timeout=5)
                time.sleep(5)
            except:
                g_logger.error("点击:{}失败".format(tab_name))
                return None
        games = []  # 返回的游戏列表

        eles = self.device.find_elements_by_xpath(self.conf.classify_tab.xpath_games, timeout=10)
        if eles:
            games = [ele.get_attribute('text') for ele in eles]
        elif check_empty:
            # 确认是否是页面没有游戏
            try:
                self.device.find_element_by_id(self.conf.loading_empty.id, timeout=10)
                g_logger.info("此分类下没有游戏")
            except:
                g_logger.error("游戏名未获取到&空分类页未找到".format(tab_name))
                return None

        return games

    def click_game_tags(self, tags_name):
        """
        点击游戏类别标签
        Args:
            tags_name: 类别标签名
        Returns:
            True: 点击成功, False: 点击失败
        """
        find_xpath = self.conf.classify_tab.xpath_game_tags.format(tags_name)
        ele = self.device.swipe_ele_find_ele(find_xpath=find_xpath, swipe_id=self.conf.classify.id_content, timeout=60)
        if ele:
            ele.click()
            time.sleep(3)
            return True
        else:
            g_logger.error("查找分类：{}失败".format(tags_name))
            return False






