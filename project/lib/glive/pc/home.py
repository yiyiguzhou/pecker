# -*- coding: UTF-8 -*-

"""
File Name:      home
Author:         zhangwei04
Create Date:    2019/7/19
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.glive.pc.common import Common
from selenium.webdriver.common.by import By

from framework.utils.selenium.action_chains import ActionChains


class Home(Common):
    def __init__(self, target, ele_conf_name='pc'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

    def into_home(self, close_recommend=True):
        """
        进入主页
        Returns:
            True: 进入成功, False: 进入失败
        """
        self.device.switch_to_last_window()
        self.device.get(self.conf.url.glive_home)
        if close_recommend:
            self.close_recommend_tips()
        try:    # 检测首页弹窗
            self.device.find_element_by_xpath("//div[@class='_ok lottery-close']", timeout=4).click()
            time.sleep(0.5)
        except:
            pass

        return True

    def click_login_button(self):
        """
        点击登录按钮
        Returns:
            False: 点击失败, True:点击成功
        """
        return self.device.click_by_xpath("//div[@class='login']/a[@data-user='login-btn']", desc="登录按钮", timeout=5)

    def click_logo(self, close_window=True):
        """
        点击爱奇艺直播logo
        Returns:
            True: 点击成功， False:点击失败
        """
        window_handles = self.device.window_handles
        if not self.device.click_by_xpath("//div[@data-node='logo']//a[@class='logo']", desc="爱奇艺logo", timeout=10):
            return False

        if len(self.device.window_handles) - len(window_handles):
            if close_window:
                g_logger.info("关闭新弹出窗口")
                self.device.close_last_window()
            return True
        return False

    def into_side_list_title(self, title):
        """
        点击侧边栏标题
        Args:
            title: 标题名
        Returns:
            True: 点击成功, False: 点击失败
        """
        xpath_title = self.conf.side_classify.xpath_subtitle.format(title)
        ele = self.device.swipe_ele_down_by_class_find_ele("scrollbar", find_type="xpath", find_text=xpath_title)
        if ele:
            try:
                ele.click()
            except:
                return g_logger.error("滑动侧边滑动栏点击标题失败")
            time.sleep(2)
        else:
            return g_logger.error("查找元素失败")
        return True

    def check_subtitle_page(self, title, timeout=6):
        """
        检测是否处于子标题页面
        Args:
            title: 子标题名
            timeout: 检测超时
        Returns:
            True: 检测成功, False: 检测失败
        """
        time_start = time.time()
        while timeout > time.time() - time_start:
            try:
                ele = self.device.find_element_by_xpath("//div[@class='wrapper']/div[@class='subtitle']/h1", timeout=2)
                text = ele.text
                g_logger.info("期望子标题：{}, 实际子标题：{}".format(title, text))
                return text == title
            except:
                self.close_recommend_tips()
        else:
            g_logger.info("查找子标题元素超时")
            return False

    def into_second_classify(self, title):
        """
        进入2级分类
        Args:
            title: 2级分类标题
        Returns:
            True: 进入成功， False, 进入失败
        """
        xpath_title = self.conf.home_classify.xpath_sub_title.format(title)
        time.sleep(2)   # 增加2秒延时
        ele = self.device.swipe_ele_down_by_class_find_ele("scrollbar", find_type="xpath", find_text=xpath_title)
        if ele:
            ele.click()
            time.sleep(2)
        else:
            g_logger.info("查找子标题：{}失败".format(title))
            return False
        return True

    def search(self, text):
        """
        搜索内容
        Args:
            text: 搜索文本，包含主播/房间号/标题
        Returns:
            True: 搜索成功, False: 搜索失败
        """
        try:
            g_logger.info("输入搜索词: {}".format(text))
            self.device.find_element_by_xpath(self.conf.home_search.xpath).send_keys(text)
            self.device.find_element_by_xpath(self.conf.home_search.button_xpath).click()
            time.sleep(2)
            return g_logger.info("点击搜索成功")
        except:
            return g_logger.error("查找搜索/点击搜索按钮失败")

    def click_follow(self):
        """
        点击我的关注推荐栏，弹出推荐cross list
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_by_xpath(self.conf.home_recommend.follow_list, time_sleep=0.5, desc="我的关注")

    def click_follow_more(self):
        """
        点击我的关注弹窗-查看更多按钮
        Returns:
        True: 点击成功, False: 点击失败
        """
        return self.device.click_by_xpath(self.conf.home_follow_list.look_more_xpath, desc="查看更多")

    def check_follow_scroll(self):
        """
        检测我的
        Returns:
            True: 检测成功, False: 检测失败
        """
        try:
            li_eles = self.device.find_elements_by_xpath(self.conf.home_follow_list.live_cross_li_xpath)
            room_msg_list = []
            for li_ele in li_eles:
                room_msg = self.format_room_cross_msg(li_ele)
                g_logger.info("直播间信息：{}".format(room_msg))
                room_msg_list.append(room_msg)
            g_logger.info("检测滑动按钮")
            self.device.find_element_by_xpath(self.conf.home_follow_list.scroll_xpath)
            g_logger.info("检测查看更多按钮")
            self.device.find_element_by_xpath(self.conf.home_follow_list.look_more_xpath)
            return True
        except:
            return g_logger.error("检测滑动弹窗元素失败")

    def follow_into_live_room(self, index=None, anchor=None, title=None):
        """
        从我的关注进入直播间
        Args:
            index: 关注直播间列表索引，从1开始
            anchor: 主播名
            title: 直播间标题
        Returns:
            True: 点击直播间成功, False: 点击直播间失败
        """
        if not index and not anchor and not title:
            return g_logger.error("参数: index, anchor, title必须传递一个")
        if index:
            find_xpath = self.conf.home_follow_list.room_index_xpath.format(index)
        elif title:
            find_xpath = self.conf.home_follow_list.title_xpath.format(title)
        else:
            find_xpath = self.conf.home_follow_list.author_xpath.format(anchor)

        ele = self.device.swipe_ele_down_by_xpath_find_ele(self.conf.home_follow_list.scroll_xpath, find_type="xpath", find_text=find_xpath)
        if ele:
            ele.click()
            time.sleep(2)
        else:
            g_logger.info("查找元素失败")
            return False
        return True

    def click_history(self):
        """
        点击观看历史推荐栏，弹出推荐cross list
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_by_xpath(self.conf.home_recommend.history_list, time_sleep=0.5, desc="观看历史")

    def click_history_more(self):
        """
        点击观看历史弹窗-查看更多按钮
        Returns:
        True: 点击成功, False: 点击失败
        """
        return self.device.click_by_xpath(self.conf.home_history_list.look_more_xpath, desc="查看更多")

    def check_history_scroll(self):
        """
        检测观看历史弹窗
        Returns:
            True: 检测成功, False: 检测失败
        """
        try:
            time.sleep(1)
            li_eles = self.device.find_elements_by_xpath(self.conf.home_history_list.live_cross_li_xpath)
            room_msg_list = []
            for li_ele in li_eles:
                room_msg = self.format_room_cross_msg(li_ele)
                g_logger.info("直播间信息：{}".format(room_msg))
                room_msg_list.append(room_msg)
            g_logger.info("检测滑动按钮")
            self.device.find_element_by_xpath(self.conf.home_history_list.scroll_xpath)
            g_logger.info("检测查看更多按钮")
            self.device.find_element_by_xpath(self.conf.home_history_list.look_more_xpath)
            return True
        except:
            return g_logger.error("检测滑动弹窗元素失败")

    def history_into_live_room(self, index=None, anchor=None, title=None):
        """
        从观看历史进入直播间
        Args:
            index: 关注直播间列表索引，从1开始
            anchor: 主播名
            title: 直播间标题
        Returns:
            True: 点击直播间成功, False: 点击直播间失败
        """
        if not index and not anchor and not title:
            return g_logger.error("参数: index, anchor, title必须传递一个")
        if index:
            find_xpath = self.conf.home_history_list.room_index_xpath.format(index)
        elif title:
            find_xpath = self.conf.home_history_list.title_xpath.format(title)
        else:
            find_xpath = self.conf.home_history_list.author_xpath.format(anchor)

        ele = self.device.swipe_ele_down_by_xpath_find_ele(self.conf.home_history_list.scroll_xpath, find_type="xpath", find_text=find_xpath)
        if ele:
            ele.click()
            time.sleep(2)
        else:
            g_logger.info("查找元素失败")
            return False
        return True

    def into_rank(self):
        """
        进入榜单页
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_by_xpath(self.conf.home_recommend.rank, desc="主播排行榜", timeout=5)

    def into_user_center(self):
        """
        从个人中心入口进入个人中心
        Returns:
            True: 点击个人中心成功, False: 点击个人中心失败
        """
        return self.device.click_by_link_text("个人中心", desc="个人中心")

    def check_charge_ui(self, check_price=False):
        """
        检测充值页UI
        Args:
            check_price: 是否检测价格
        Returns:
            True: 检测成功, False: 检测失败
        """
        if not self.device.check_ele_by_xpath(self.conf.home_charge_page.title):
            return g_logger.error("检测充值页面标题失败")
        if not self.device.check_ele_by_id(self.conf.home_charge_page.qidou_list_id):
            return g_logger.error("检测充值页奇豆列表ID失败")
        if check_price:
            li_eles = self.device.find_elements_by_xpath(self.conf.home_charge_page.li)
            if not li_eles:
                return g_logger.error("读取充值奇豆列表元素失败")
            qidou_list = [self._format_charge_qidou_msg(ele) for ele in li_eles]    # 奇豆信息列表
            g_logger.info("奇豆充值列表信息：{}".format(qidou_list))
            if not qidou_list[0]['select']:
                return g_logger.error("奇豆最小值不是默认选项")
            qidou_num = [item['number'] for item in qidou_list]
            price = [item['price'] for item in qidou_list]

        return True

    def _format_charge_qidou_msg(self, li_ele):
        """
        格式化奇豆充值信息
        Args:
            li_ele: 奇豆充值列表元素实例
        Returns:
            dict: 充值奇豆字典，价格price，数量number, 是否被选择select
        """
        li_dict = {"price": None, "number": None, "select": False}
        cls = li_ele.get_attribute("class")
        if cls:
            li_dict['select'] = "selected" in cls
        try:
            li_dict["price"] = li_ele.find_element_by_xpath(self.conf.home_charge_page.li_money).text
            li_dict["number"] = li_ele.find_element_by_xpath(self.conf.home_charge_page.li_qidou_num).text
        except Exception as e:
            g_logger.warning("格式化读取奇豆部分信息失败")
        return li_dict

    def click_charge_button(self):
        """点击充值按钮
        Returns:
            True: 点击成功, False: 点击失败
        """
        if self._move_to_user_center():
            return self.device.click_by_xpath(self.conf.home_user.charge, desc="充值按钮")
        return False

    def click_user_icon(self):
        """
        点击用户图标
        Returns:
            True: 点击成功, False: 点击失败
        """
        if self._move_to_user_center():
            return self.device.click_by_xpath(self.conf.home_user.icon, time_sleep=2, desc='用户图标')
        return False

    def _move_to_user_center(self):
        """移动到个人中心"""
        self.close_recommend_tips()
        try:
            ele = self.device.find_element_by_link_text("个人中心")
            self.device.move_to_element(ele)
            time.sleep(1)
            return True
        except:
            return g_logger.error("未找到个人中心")

    def into_anchor(self):
        """
        进入主播页，
        PS:需要主播账户登录，点击主播相关按钮进入
        Returns:
            True: 进入成功, False: 进入失败
        """
        if not self.device.click_by_partial_link_text("主播相关"):
            self.close_recommend_tips()
            return self.device.click_by_partial_link_text("主播相关")
        return True
