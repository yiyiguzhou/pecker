# -*- coding: UTF-8 -*-

"""
File Name:      homepage
Author:         gufangmei_sx
Create Date:    2018/8/14
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from project.lib.gamecenter.android.smoke.common import Common
from appium.webdriver.common.touch_action import TouchAction


class HomePage(Common):
    """推荐页，游戏中心默认进入页"""
    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

        self.target = target
        self.data = target.data
        self.device = target.device

    def check_ui(self, timeout=120):
        """
        检测推荐页UI
        Returns:
            True: 检测成功, False: 检测失败
        """
        return self.device.swipe_find_ele_by_xpath(xpath="//android.widget.TextView[@text='新游']", direct="down", rate=0.6, timeout=timeout)

    def into_poker(self, special_topic=None):
        """
        点击棋牌图标
        Args:
            special_topic: 页面标题
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_xpath(self.conf.gamecenter_poker.xpath, timeout=5, desc="点击棋牌图标")
            time.sleep(5)
            if special_topic:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_topic), timeout=10)
        except:
            return False
        return True

    def into_configurable_entrance(self, entrance_num, check_desc=None):
        """
        进入子业务可配置入口
        Args:
            entrance_num: 可配置入口号
            check_desc: 确认进入业务入口描述
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.click_by_xpath(self.conf.gamecenter_subservice_configurable_entrance.xpath.format(entrance_num), timeout=10)
            time.sleep(5)
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(check_desc), timeout=5)
        except Exception as e:
            return False
        self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'], "entrance_{}_sucess.png".format(entrance_num)))
        return True

    def game_center_search(self, search_text=''):
        """
        游戏中心页面搜索操作
        Args:
            search_text: 搜索文本
        Returns:
            True: 搜索成功
            False: 搜索失败
        """
        try:
            self.device.click_by_id('com.qiyi.gamecenter:id/common_title_right_search_ly', timeout=5, desc="点击页面搜索框")
            time.sleep(1)
            self.device.find_element_by_id(self.conf.gamecenter_search_input.id, timeout=5).send_keys(search_text)
            time.sleep(2)
            self.device.hide_keyboard()
            self.device.click_by_xpath("//{}[@text='{}']".format(self.conf.gamecenter_search_game.cls, search_text), timeout=5, desc="点击{}游戏icon进入详情页".format(search_text))
            time.sleep(3)
            # self.device.click_by_xpath("//{}[@text='{}']".format(self.conf.gamecenter_search_game.cls, search_text), timeout=5, desc="点击搜索")
            # time.sleep(3)

        except Exception as e:
            return False
        return True

    def game_search_click_icon(self, game_name):
        """
        搜索游戏，并点击图表进入游戏详情
        Args:
            game_name: 搜索游戏名
        Returns:

        """
        try:
            self.device.click_by_id('com.qiyi.gamecenter:id/common_title_right_search_ly', timeout=5, desc="点击页面搜索框")
            time.sleep(1)
            self.device.find_element_by_id(self.conf.gamecenter_search_input.id, timeout=5).send_keys(game_name)
            time.sleep(1)
            self.device.hide_keyboard()
            try:
                self.device.click_by_xpath(self.conf.gamecenter_search_game.xpath_icon.format(game_name), timeout=5)
                time.sleep(2)
                g_logger.info("游戏无联想词，返回成功")
                return True
            except:
                try:
                    self.device.click_by_xpath("//{}[@text='{}']".format(self.conf.gamecenter_search_game.cls, game_name), timeout=5)
                    time.sleep(2)
                    self.device.click_by_xpath(self.conf.gamecenter_search_game.xpath_icon.format(game_name), timeout=5)
                    time.sleep(2)
                    return True
                except:
                    g_logger.error("点击两次搜索名 查找游戏失败")
                    return False
        except:
            g_logger.error("游戏搜索失败")

    def into_detail_page(self):
        """
        游戏中心-点击焦点图进入游戏详情界面
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.tap([(540, 445)])
        except:
            return False
        return True

    def _large_picture_into(self, find_xpath, timeout=240):
        """
        大图模块进入
        Args:
            find_xpath:

        Returns:

        """

        ele = self.device.swipe_down_find_ele(xpath=find_xpath, timeout=timeout)
        if ele:
            try:
                bottom_ele = self.device.find_element_by_id(self.conf.home_bottom.id, timeout=5)
                if self.device.check_ele_on_ele(ele, bottom_ele):
                    g_logger.info("检测到元素和底部栏重叠，向上滑动0.3")
                    self.device.swipe_screen(rate=0.3, sleep_time=3)
                    ele = self.device.find_element_by_xpath(find_xpath, timeout=10)
            except:
                g_logger.warning("检测底部栏元素重叠时，查找底部栏失败")
                return False
            ele.click()
            time.sleep(3)
            return True
        else:
            g_logger.info("查找xpath元素：{}失败".format(find_xpath))
            return False

    def large_picture_with_game_into(self, game_introduction, timeout=360):
        """
        游戏中心-点击大图进入游戏详情界面
        Args:
            game_introduction: 游戏中心大图详情页标语
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)
        find_xpath = "//android.widget.TextView[@text='{}' and @resource-id='com.qiyi.gamecenter:id/huge_image_game_name']".format(game_introduction)
        return self._large_picture_into(find_xpath, timeout=timeout)

    def large_picture_without_game_into(self, desc, timeout=360):
        """
        游戏中心-点击大图进入H5页面
        Args:
            desc: 游戏中心大图详情页标语
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)
        find_xpath = "//android.widget.TextView[@text='{}' and @resource-id='com.qiyi.gamecenter:id/huge_image_desc']".format(desc)
        return self._large_picture_into(find_xpath, timeout=timeout)

    def into_my_game_module(self, my_module, tab):
        """
        游戏中心-我的游戏模块
         Args:
            my_module: 查看全部我的游戏
            tab: 玩过tab
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            time.sleep(2)
            self.device.click_by_xpath("//android.widget.TextView[@text='{}']".format(my_module), timeout=5, desc="点击查看全部我的游戏按钮")
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(tab), timeout=5)
        except:
            return False
        return True

    def into_small_game_module(self):
        """
        游戏中心-小游戏模块
        Returns:
            True: 进入成功
            False：进入失败
        """
        small_entry = "//android.widget.LinearLayout[@resource-id='com.qiyi.gamecenter:id/layout_h5_games']/android.widget.ImageView[@resource-id='com.qiyi.gamecenter:id/template_list_more']"
        try:
            self.device.click_by_xpath(small_entry, timeout=5, desc='进入小游戏入口')
            self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺小游戏']", timeout=30)
            time.sleep(3)
        except:
            g_logger.error("进入小游戏失败")
            return False
        return True

    def click_first_position(self, game_name, game_information):
        """
        点击横排游戏的第一个运营位
        Args:
            game_name: 游戏名
            game_information:游戏详情页信息
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
            (x2, y2) = self.get_location_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
            self.device.tap([(x2+100, y2+200)])
            self.check_title(game_information)
        except:
           return False
        return True

    def click_game_horizontal_first_icon(self, title):
        """
        点击横排游戏专题推荐第一个运营位
        Args:
            title: 标题名
        Returns:
            True: 进入成功
            False：进入失败
        """
        first_game_icon_xpath = "//android.widget.TextView[@text='{}']/../../../../..//android.widget.ImageView[@resource-id='com.qiyi.gamecenter:id/game_icon']".format(
            title)
        return self.click_special_first_icon(title, first_game_icon_xpath)

    def click_picture_horizontal_first_icon(self, title):
        """
        点击横排图片专题推荐第一个运营位
        Args:
            title: 标题名
        Returns:
            True: 进入成功
            False：进入失败
        """
        first_pic_icon_xpath = "//android.widget.TextView[@text='{}']/../../../../..//android.widget.ImageView[@resource-id='com.qiyi.gamecenter:id/horizontal_image_item_icon']".format(title)
        return self.click_special_first_icon(title, first_pic_icon_xpath)

    def click_special_first_icon(self, title, click_xpath):
        """
        点击专题推荐第一个运营位
        Args:
            title: 标题名
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)

        ele = self.device.swipe_find_ele_by_xpath(click_xpath, timeout=120)
        if ele:
            g_logger.info("点击标题：{} 下方第一个图标".format(title))
            ele.click()
            time.sleep(2)
            return True
        else:
            return False

    def click_horizontal_pic_first(self, title):
        """
        点击横排图片模块第一个图片
        Args:
            title: 横排模块标题
        Returns:
            True: 点击成功， False: 点击失败
        """
        first_icon_xpath = self.conf.horizontal_pic_template.xpath_first_icon.format(title)
        ele = self.device.swipe_down_find_ele(xpath=first_icon_xpath, rate=0.2, timeout=60)
        if ele:
            ele.click()
            time.sleep(3)
            return True
        else:
            g_logger.error("查找横排图片模块:{}的第一张图片失败".format(first_icon_xpath))
            return False

    def game_list_look_all(self, title, special_topic):
        """
        点击游戏列表--查找全部按钮
        Args:
            title: 游戏列表标题
            special_topic: 进入后页面标题
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')

        # 滑动查找列表下方信息
        for i in range(10):
            try:
                time.sleep(2)
                self.device.click_by_xpath(self.conf.gamecenter_game_list_all.xpath.format(title), timeout=5, desc="点击查找全部按钮")
                time.sleep(2)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(special_topic), timeout=5)
                time.sleep(3)
                break
            except:
                if i == 9:
                    g_logger.error("查找失败")
                    return False

                self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 2 / 5)
                continue
        return True

    def into_small_game(self):
        """
        进入游戏中心小游戏
         Returns:
            True: 进入成功
            False：进入失败
         """
        pic_path = os.path.join(g_resource['testcase_log_dir'],"into_small_game_faied_{}.png".format(g_resource['testcase_loop']))

        try:
            size = self.device.get_window_size()
            width = size.get('width')
            height = size.get('height')

            self.device.tap([(width * 0.21, height * 0.22)])
            time.sleep(10)

            try:
                text = self.device.find_element_by_id('com.qiyi.gamecenter:id/actionBar_title').get_attribute('text')
                if 'H5游戏' not in text:
                    self.device.adb.screen_shot(pic_path)
                    return False
            except:
                self.device.adb.screen_shot(pic_path)
                return False
        except:
            self.device.adb.screen_shot(pic_path)
            return False

    def click_reservation_button(self, game_name, promt, open_icon):
        """
        点击预约按钮
        Args:
            game_name: 游戏名
            promt: 提示语
            open_icon: 按钮名
        Returns:
            True: 进入成功
            False：进入失败
        """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')
        game_name_list = game_name if isinstance(game_name, list) else [game_name]

        def __look_for_ganme():
            """内部函数:查找游戏,并点击游戏的预约按钮"""
            for i in range(6):
                for game_n in game_name_list:
                    try:
                        self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_n), timeout=5)
                        reser_xpath = "//android.widget.TextView[@text='{}']/../../android.widget.FrameLayout".format(game_n)  # 通过游戏名位置定位到对应的预约图标模块
                        self.device.click_by_xpath(reser_xpath, timeout=5, desc="通过游戏名点击预约按钮")
                        time.sleep(2)
                        return True
                    except:
                        pass
                if i == 5:
                    g_logger.info('游戏: {}'.format(",".join(game_name_list)))
                    return False
                self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
                time.sleep(1)

        if not __look_for_ganme():
            return False

        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(promt), timeout=5)
            self.device.click_by_id("//android.widget.Button[@text='{}']".format(open_icon), timeout=5)
            g_logger.info('成功预约')
            return True
        except:
            g_logger.info('该游戏已预约')
            return True

    def click_reserved_button(self, game_name, promt):
        """
        点击已预约按钮
        Args:
            game_name: 游戏名
            promt: 提示语
        Returns:
            True: 进入成功
            False：进入失败
        """
        try:
            (x, y) = self.get_location_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
            self.device.tap([(x + 270, y)])
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(promt), timeout=5)
            g_logger.info('未预约成功')
            return False
        except:
            g_logger.info('已预约')
            return True

    def into_new_game(self):
        """
        游戏中心进入新游
        Returns:
            True: 搜索成功
            False: 搜索失败
         """
        ele = self._stable_element(xpath=self.conf.gamecenter_newgame.xpath, timeout=20)
        if ele:
            ele.click()
            g_logger.info("点击新游入口")
            time.sleep(2)
            return True
        else:
            g_logger.info("查找新游失败")
            return False

    def check_newgame_online_tab(self):
        """
        新游页--按顺序检查今日新游，本月新游，季度新游
        Returns:
            True: 搜索成功
            False: 搜索失败
         """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')
        # try:
        #     self.device.find_element_by_xpath("//android.widget.TextView[@text='今日新游']", timeout=5)
        # except:
        #     g_logger.info('无今日新游模块')
        #     pass

        ret = True
        for i in range(20):
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='本月新游']", timeout=5)
                g_logger.info("找到本月新游")
                time.sleep(2)
                break
            except:
                if i == 19:
                    g_logger.info('无本月新游模块')
                    ret = False

                self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
                time.sleep(1)
                continue

        for i in range(30):
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='季度新游']", timeout=5)
                g_logger.info("找到季度新游")
                time.sleep(2)
                break
            except:
                if i == 29:
                    g_logger.info('无季度新游模块')
                    ret = False

                self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
                time.sleep(1)
                continue
        return ret

    def check_latest_reservation(self, game1, game2, game3):
        """
        新游页--检查最新预约tab的上方三个游戏
        Args:
            game1: 第一款游戏名
            game2: 第二款游戏名
            game3: 第三款游戏名
        Returns:
            True: 搜索成功
            False: 搜索失败
         """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game1), timeout=5)
        except:
            return False

        for i in range(3):
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game2), timeout=5)
                time.sleep(2)
                break
            except:
                if i == 2:
                    return False

                self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
                time.sleep(1)
                continue

        for i in range(5):
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game3), timeout=5)
                time.sleep(4)
                break
            except:
                if i == 29:
                    return False

                self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
                time.sleep(1)
                continue
        return True

    def check_sealing_game(self, game_name, timeout=10):
        """
        新游页--检查封测专区tab的两款游戏
        Args:
            game_name: 游戏名列表
            timeout: 检测超时
        Returns:
            True: 搜索成功
            False: 搜索失败
         """
        try:
            ele = self.device.find_element_by_id(self.conf.loading_empty.id, timeout=5)
            g_logger.info("新游-封测专区：{}".format(ele.get_attribute("text")))
            return True
        except:
            return self.check_title(game_name, timeout=timeout)

    def game_center_into_list_page(self):
        """
        游戏中心进入榜单页
        Returns:
            True: 搜索成功
            False: 搜索失败
         """
        try:
            time.sleep(3)
            self.device.click_by_xpath("//android.widget.TextView[@text='榜单']", timeout=10, desc="点击榜单按钮")
            self.device.find_element_by_xpath("//android.widget.TextView[@text='排行榜']", timeout=5)
        except:
            return False
        return True

    def check_game_order(self, game_name_list):
        """
        检查游戏顺序
        Args:
            game_name_list: 配置的游戏列表
        Returns:
            True: 搜索成功
             False: 搜索失败
        """
        if not isinstance(game_name_list, list):
            g_logger.error("请至少配置第一页两款游戏")
            return False

        y_pos_list = []
        for game_name in game_name_list:
            try:
                x, y = self.get_location_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=10)
                y_pos_list.append(y)
            except:
                g_logger.error("未找到游戏：{}".format(game_name))
                return False

        sort_y_pos_list = sorted(y_pos_list)
        if not sort_y_pos_list == y_pos_list:
            g_logger.error("游戏序列和实际排行不匹配: {}".format(",".join(game_name_list)))
            return False

        return True

    def check_game_details(self):
        """
        游戏详情页--显示详情、福利、圈子三个tab
        Returns:
            True: 搜索成功
            False: 搜索失败
         """
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='详情']", timeout=5)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='福利']", timeout=5)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏圈']", timeout=5)
            return True
        except:
            return False

    def swipe_down_into_game_detail(self, game_name, click_icon=False, check_text=None):
        """
        向下滑动寻找游戏并进入详情页,（通过游戏名点击游戏图片进入详情页），
        备注：不要使用与默认搜索框同名的游戏，否则会进入搜索框
        Args:
            game_name: 游戏名
            click_icon: 是否根据icon点击进入游戏详情页
            check_text: 进入游戏详情页后，检测的文本，确保进入了游戏详情页
        Returns:
            True: 进入游戏详情页成功
            False: 进入失败
         """
        if click_icon:
            xpath = "//android.widget.TextView[@text='{}']/../android.widget.RelativeLayout[@resource-id='com.qiyi.gamecenter:id/horizontal_game_item_icon']".format(game_name)
        else:
            xpath = "//android.widget.TextView[@text='{}']".format(game_name)
        ele = self.device.swipe_down_find_ele(xpath=xpath, timeout=120)
        if ele:
            try:
                bottom_ele = self.device.find_element_by_id(self.conf.home_bottom.id, timeout=10)
                if self.device.check_ele_on_ele(ele, bottom_ele):
                    g_logger.info("元素处于底部，向上滑动，防止重叠")
                    self.device.swipe_screen(rate=0.3)
                    time.sleep(2)
                    # ele = self.device.find_element_by_xpath(xpath, timeout=10)
            except Exception as e:
                pass
            ele = self.device.swipe_down_find_ele(xpath=xpath, timeout=120)

            if ele:
                try:
                    g_logger.info("{}图标，位置，{}, 大小{}".format(game_name, ele.location, ele.size))
                except:
                    pass
                ele.click()
                time.sleep(5)
            else:
                return False
        else:
            return False
        # if not ele:
        #     return False
        # else:
        #     g_logger.info("{}图标，位置，{}, 大小{}".format(game_name, ele.location, ele.size))
        #     ele.click()
        #     time.sleep(5)  # 等待5秒，待页面加载完成，稳定下来

        if check_text:  # 检测进入后的信息
            return self._swipe_down_check_text(check_text)
        return True

    def search_game_name(self, game_name):
        """
        寻找游戏并进入详情页,（通过点击游戏名进入详情页）
        Args:
            game_name: 游戏名
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')

        # 滑动查找游戏详细信息
        for i in range(10):
            try:
                self.device.click_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=5)
                time.sleep(2)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name),timeout=5)
                break
            except:
                if i == 9:
                    return False

                self.device.swipe(width / 2, height * 3 / 4, width / 2, height * 1 / 4)
                time.sleep(1)
                continue
        return True

    def check_video(self, game_name=None):
        """
        check视频播放
        Args:
            game_name: 视频游戏名称
        Returns:
            True: 搜索成功
            False: 搜索失败
        """
        # video_xpath = self.conf.video_play.xpath.format(introduction)
        full_screen_flag = False
        try:
            try:
                self.device.click_by_id(self.conf.video_play_tolandscape.id, timeout=5, desc="点击全屏按钮")
                # self.device.click_by_xpath(self.conf.video_play_tolandscape.xpath, timeout=5, desc="点击全屏按钮")
                time.sleep(0.5)
            except:
                g_logger.info("底部栏消失，通过坐标点击方式调起底部栏")
                self.device.tap([(540, 100)])
                self.device.click_by_id(self.conf.video_play_tolandscape.id, timeout=5, desc="点击全屏按钮")

            full_screen_flag = True

            self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'], "play_video_tolandscape.png"))
            try:
                self.device.click_by_id(self.conf.video_play_pause.id, timeout=5, desc="点击暂停按钮")
            except:
                g_logger.info("底部栏消失，通过坐标点击方式调起底部栏")
                self.device.tap([(540, 540)])
                self.device.click_by_id(self.conf.video_play_pause.id, timeout=5, desc="点击暂停按钮")

            time.sleep(1)
            self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video_pause.png"))
            try:
                self.device.click_by_id(self.conf.video_play_pause.id, timeout=5, desc="点击播放按钮")
            except:
                g_logger.info("底部栏消失，通过坐标点击方式调起底部栏")
                self.device.tap([(540, 540)])
                # time.sleep(0.2)
                self.device.click_by_id(self.conf.video_play_pause.id, timeout=5, desc="点击播放按钮")
            # 退出全屏视频播放
            time.sleep(0.5)
            self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video_again.png"))
            self.device.keyevent(4)
            time.sleep(1)
            self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "play_video_tolandscape_back.png"))
            return True
        except:
            return full_screen_flag

    def check_top_bar_title(self):
        """
        查看顶部栏显示标题
        Returns:
            True: 搜索成功
            False: 搜索失败
         """
        try:
            size = self.device.get_window_size()
            width = size.get('width')
            height = size.get('height')
            self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
            time.sleep(2)
            self.device.find_element_by_id(self.conf.gamecenter_game_title.id, timeout=5)
        except:
            return False
        return True

    def click_first_video_template(self, game_name):
        """
        点击视频模板运营位的播放按钮
        Args:
            game_name: 带视频游戏名
        Returns:
            True: 搜索成功
            False: 搜索失败
        """
        video_xpath = self.conf.gamecenter_video.xpath.format(game_name)

        if not self.device.swipe_down_find_ele(xpath=video_xpath, timeout=120):
            g_logger.error("查找游戏视频失败")
            return False

        try:
            # 按钮会自动播放
            self.device.click_by_id(self.conf.video_play.id, timeout=5, desc="点击视频播放按钮")
        except:
            try:
                self.device.click_by_xpath(video_xpath, timeout=5, desc="视频已播放，点击视频弹出底边栏")
            except:
                return False
        return True

    def video_template_goto_game_detail(self, game_name):
        """
        从视频模块进入游戏详情页
        Args:
            game_name: 带视频的游戏名
        Returns:
            True: 找到视频模块，并点击游戏名进入详情页
        """
        game_xpath = self.conf.video_game.xpath.format(game_name)
        ele = self.device.swipe_down_find_ele(xpath=game_xpath, timeout=60)
        if not ele:
            g_logger.error("查找带视频的游戏{}失败".format(game_name))
            return False
        else:
            time.sleep(2)
            self.device.click_by_xpath(game_xpath, timeout=5, desc='点击进入游戏详情页')
            time.sleep(5)
        return True

    def click_h5_picture(self, game_name, ele):
        """
        点击H5页面上的游戏图片进入游戏中心的游戏详情页并查看
        Args:
            game_name: 游戏名
            ele: 页面上某一元素的text
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')

        # 滑动查找某个按钮
        for i in range(5):
            try:
                self.device.find_element_by_xpath("//android.view.View[@content-desc='{}']".format(game_name), timeout=5)
                (x, y) = self.get_location_by_xpath("//android.view.View[@content-desc='{}']".format(game_name), timeout=5)
                g_logger.info((x, y-200))
                if (y-200<0):
                    self.device.swipe(width / 2, height * 1 / 6, width / 2, height * 3 / 6)
                    (x, y) = self.get_location_by_xpath("//android.view.View[@content-desc='{}']".format(game_name), timeout=5)
                else:
                    pass
                self.device.tap([(x, y-200)])
                time.sleep(2)
                break
            except:
                if i == 4:
                    return False

                self.device.swipe(width / 2, height * 3 / 5, width / 2, height * 1 / 5)
                time.sleep(1)
                continue
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(ele), timeout=5)
            time.sleep(2)
        except:
            return False
        return True

    def check_search_default_text(self, text_list):
        """
        检查搜索栏默认配置搜索词
        Args:
            text_list: 后台配置的默认文本列表
        Returns:
            True: 检查成功，False: 检查失败
        """
        try:
            ele = self.device.find_element_by_id("com.qiyi.gamecenter:id/common_title_right_search_tv", timeout=30)
        except:
            g_logger.error("查找搜索栏失败")
            return False
        if not isinstance(text_list, list):
            text_list = [text_list]
        return ele.get_attribute("text") in text_list

    def check_focus_ui(self):
        """检测轮播图UI，检测点：元素布局，元素内容
        Returns
            True: 检测成功，False: 检测失败
        """
        try:
            self.device.find_element_by_id("com.qiyi.gamecenter:id/banner_image", timeout=20)  # 图片id
            return True
        except Exception as e:
            g_logger.error("未找到轮播图的元素id")
            return False

    def check_focus_refresh(self, title_sort):
        """检测焦点图/轮播图UI，检测点：元素布局，元素内容
        Args:
            title_sort: 标题顺序
        Returns
            True: 检测成功，False: 检测失败
        """
        if not isinstance(title_sort, list):
            title_sort = [title_sort]
        main_title_set = list()
        sub_title_set = list()
        try:
            start_x, start_y, end_x, end_y = self.device.get_ele_swpie_coordinate(swipe_id="com.qiyi.gamecenter:id/banner_image", direction="left", rate=0.8)
            for i in range(10):
                main_title = self.device.find_element_by_id("com.qiyi.gamecenter:id/banner_main_title", timeout=2).get_attribute("text")
                if main_title in main_title_set:
                    break
                main_title_set.append(main_title)
                sub_title = self.device.find_element_by_id("com.qiyi.gamecenter:id/banner_sub_title", timeout=2).get_attribute("text")
                if sub_title in sub_title_set:
                    break
                sub_title_set.append(sub_title)
                self.device.swipe(int(start_x), int(start_y), int(end_x), int(end_y))
        except Exception as e:
            return False

        for sub, main in zip(sub_title_set, main_title_set):
            g_logger.info("标题：{}， 子标题: {}".format(main, sub))
        if title_sort[0] in main_title_set:
            index = main_title_set.index(title_sort[0])
            revise_title_set = main_title_set[index:] + main_title_set[0: index]
        else:
            g_logger.warning("期望值与实际值不匹配")
            g_logger.warning("期望值: {}".format(title_sort))
            g_logger.warning("实际值: {}".format(main_title_set))
            return False
        return revise_title_set == title_sort

    def check_horizontal_game(self, title):
        """
        检测横排游戏，是否最多显示10个游戏
        Args:
            title: 横排标题
        Returns:
            True: 检测成功，False: 检测失败
        """
        game_list = self.horizontal_get_game_list(title)
        if len(game_list) == 10:
            return True
        elif len(game_list) == 0:
            return False
        else:
            g_logger.error("横排游戏数不等于10个，检测失败")
            return False

    def check_sealing_test_game_list(self, title, game_num):
        """
        检测封测专区模块游戏列表
        Args:
            title: 列表标题
        Returns:
            True: 检测成功，False: 检测失败
        """
        game_xpath = self.conf.vertical_game_list.xpath_testting_games.format(title)
        return self.check_vertical_game_list(title, game_xpath=game_xpath, game_num=game_num, timeout=120)

    def check_vertical_game_list(self, title, game_xpath=None, game_num=None, timeout=120):
        """
        检测纵向游戏列表
        Args:
            title: 列表标题
            game_xpath: 期望游戏数量，默认是None
            game_num: 游戏数量
            timeout: 超时
        Returns:
            True: 检测成功，False: 检测失败
        """
        ele_name_list = self.vertical_get_game_list(title, game_xpath=game_xpath, timeout=timeout)
        if not isinstance(ele_name_list, list):
            return False
        if game_num:
            game_num = int(game_num)
            if game_num > 3:
                try:
                    self.device.find_element_by_xpath(self.conf.vertical_game_list.xpath_look_all.format(title), timeout=5)
                    g_logger.info("配置的游戏数量为{}, 检测全部游戏按钮成功".format(game_num))
                    return len(ele_name_list) == 3
                except:
                    g_logger.info("配置的游戏数量为{}, 未找到查看全部游戏按钮".format(game_num))
                    return False
            else:
                return len(ele_name_list) <= 3
        else:
            try:
                self.device.find_element_by_xpath(self.conf.vertical_game_list.xpath_look_all.format(title), timeout=5)
                return len(ele_name_list) == 3
            except:
                return len(ele_name_list) < 3

    def vertical_get_game_list(self, title, game_xpath=None, timeout=120):
        """
        纵向获取游戏列表
        Args:
            title: 标题
            timeout: 超时
            game_xpath: 游戏名xpath
        Returns:
            list: 游戏列表 False: 获取失败
        """
        if not self.vertical_full_on_screen(title, timeout=timeout):
            return False
        find_xpath = game_xpath if game_xpath else self.conf.vertical_game_list.xpath_games.format(title)
        eles = self.device.find_elements_by_xpath(find_xpath, timeout=10)
        if not eles:
            g_logger.error("获取{}标题的游戏名失败".format(title))
            return False

        ele_name_list = [ele.get_attribute("text") for ele in eles]
        g_logger.info(", ".join(ele_name_list))
        return ele_name_list

    def vertical_full_on_screen(self, title, timeout=120):
        """
        纵向游戏列表全屏显示
        Args:
            title: 纵向列表标题
        Returns:
            True: 查找成功， False: 查找失败
        """
        if not self.device.check_textview_text(title, swipe=True, timeout=timeout):
            g_logger.error("查找纵排标题：{} 失败".format(title))
            return False
        ele = self.device.swipe_down_find_ele(xpath=self.conf.vertical_game_list.xpath_bottom_line.format(title), timeout=60, rate=0.1)
        if not ele:
            g_logger.error("查找纵排标题底部栏：{} 失败".format(title))
            return False
        return True

    def check_entrance_config(self, name, img_path=None):
        """
        检测子业务入口配置
        Args:
            name: 可配置入口名称
            img_path: 可配置入口图像

        Returns:
            True: 检测成功， False: 检测失败
        """
        if not self.device.check_textview_text(name, timeout=10):
            return False

        if img_path:
            screen_img_path = os.path.join(self.conf_img_dir, "screen.png")
            self.device.get_screenshot_as_file(screen_img_path)
            cmp_result = self.match_image(screen_img_path, img_path)
            return cmp_result

        return True

    def reservation_into(self, game_name, timeout=60):
        """
        推荐模块进入详情页（游戏详情页、h5活动页）
        Args:
            game_name: 游戏名
            timeout: 查找超时

        Returns:
            True: 找到游戏，并点击进入， False: 未找到
        """
        if not self.reservation_full_screen(timeout=timeout):
            return False
        swipe_xpath = self.conf.home_reservation.xpath_swipe
        game_xpath = self.conf.home_reservation.xpath_game.format(game_name)
        ele = self.device.swipe_ele_find_ele(swipe_xpath=swipe_xpath, find_xpath=game_xpath, direction="left", rate=0.5, timeout=30)
        if not ele:
            g_logger.error("预约模板查找游戏：{}失败".format(game_name))
            return False
        else:
            ele.click()
            time.sleep(3)

        return True

    def reservation_look_more(self, timeout=120):
        """
        预约模板查看更多进入新游页最新预约tab
        Args:
            timeout: 查找超时
        Returns:
            True: 跳转成功，False: 跳转失败
        """
        ele = self.device.swipe_down_find_ele(xpath=self.conf.home_reservation.xpath_more, timeout=timeout)
        if ele:
            try:
                ele_floating = self.device.find_element_by_id(self.conf.home_floating.id, timeout=5)
                self.device.click_by_id(self.conf.home_floating.id_close, desc='点掉悬浮框', timeout=5)
                time.sleep(3)
            except:
                # 首页没有悬浮窗
                pass
            ele = self.device.swipe_down_find_ele(xpath=self.conf.home_reservation.xpath_more, timeout=10)
            if ele:
                ele.click()
                time.sleep(2)
                return True
            else:
                return False
        else:
            return False

    def reservation_full_screen(self, timeout=60):
        """
        滑动到预约模块全部显示
        Args:
            timeout: 查找超时
        Returns:
            True: 查找成功， False: 查找失败
        """
        if not self.device.check_textview_text(self.conf.home_reservation.title, swipe=True, timeout=timeout) or \
                not self.device.swipe_down_find_ele(xpath=self.conf.home_reservation.xpath_res_button, rate=0.2, timeout=timeout):
            g_logger.error("查找预约模板失败")
            return False
        return True

    def get_home_bottom_list_name(self):
        """
        获取底部栏元素名字里列表
        Returns:
            list: 元素列表 False: 查找底部栏元素失败
        """
        eles = self.device.find_elements_by_xpath(self.conf.home_bottom.xpath_names, timeout=10)
        if not eles:
            g_logger.error("查找底部栏失败")
            return False
        return [ele.get_attribute('text') for ele in eles]

    def check_home_bottom_ui(self, name_list):
        """
        检测底部栏UI，主要是针对底部栏元素名字列表检测
        Args:
            name_list: 游戏列表
        Returns:
            True: 检测成功， False: 检测失败
        """
        names = self.get_home_bottom_list_name()
        g_logger.info("期望值：{}".format(",".join(name_list)))
        g_logger.info("实际值：{}".format(",".join(names)))
        return names == name_list if names else False

    def full_screen_close(self):
        """
        全屏弹窗关闭
        Returns:
            True: 找到全局弹窗，并点击了关闭， False: 未找到全局弹窗
        """
        self.woman_point_out_close()
        try:
            self.device.find_element_by_id(self.conf.full_screen.id_img, timeout=10)
            self.device.click_by_id(self.conf.full_screen.id_close, timeout=5)
            time.sleep(1)
            return True
        except:
            g_logger.error("未找到全屏弹窗")
            return False

    def full_screen_download(self, game_name=None, game_type='native', uninstall=True):
        """
        全屏弹窗下载游戏
        Args:
           game_name: 游戏名称
           game_type: 游戏类型，若是"native"则下载游戏，若是"h5"则进入H5游戏
           uninstall: 安装完成后是否卸载游戏
        Returns:
           True: 找到全局弹窗，并点击了关闭， False: 未找到全局弹窗
        """
        self.woman_point_out_close()
        try:
            self.device.find_element_by_id(self.conf.full_screen.id_img, timeout=10)
            self.device.click_by_id(self.conf.full_screen.id_download, timeout=5)
        except:
            g_logger.error("未找到全屏弹窗")
            return False
        if game_type == "native":
            # 游戏下载
            g_logger.info("native游戏，下载安装后进入")
            if self.game_install(game_name, open_game=True):
                time.sleep(3)
                self.device.get_screenshot_as_file(os.path.join(g_resource["testcase_log_dir"], "native_game_screenshot.png"))
                if uninstall:
                    self.uninstall_app(app_name=game_name)
                if self.device.get_manufacturer() == 'xiaomi':
                    try:
                        self.device.click_by_xpath(self.conf.common_button.xpath_done, timeout=10)
                        time.sleep(2)
                    except:
                        pass
                return True
        elif game_type == "h5":
            # 进入H5游戏
            g_logger.info("h5游戏，直接进入")
            if self.target.H5Page.check_game_ui():
                time.sleep(3)
                self.device.get_screenshot_as_file(os.path.join(g_resource["testcase_log_dir"], "h5_game_screenshot.png"))
        return False

    def full_screen_goto_game_detail(self):
        """
        全屏弹窗下载游戏
        Returns:
           True: 找到全局弹窗，并点击了关闭， False: 未找到全局弹窗
        """
        self.woman_point_out_close()
        try:
            ele = self.device.find_element_by_id(self.conf.full_screen.id_img, timeout=10)
            x, y = ele.location['x'], ele.location['x']
            width, height = ele.size['width'], ele.size['height']
            self.device.tap([(x+width/2, y+height/2)])
            time.sleep(3)
            return True
        except:
            g_logger.error("未找到全屏弹窗")
            return False

    def check_full_screen_not_pull(self, check_text):
        """
        检测全屏弹窗未被弹出来
        Args:
            check_text: 检测文本
        Returns:
            True: 检测成功， False: 检测失败
        """
        self.woman_point_out_close()
        # google手机 全屏弹窗点击后，页面捕获卡住
        if self.device.get_manufacturer() == 'google':
            if self.device.get_window_height() in (2712, 2880):
                return self.match_any_image_to_screen(os.path.join(self.conf_img_dir, 'new_game_icon_2880.png'), timeout=10)
        return self.device.check_textview_text(check_text, timeout=10)

    def woman_point_out_close(self, timeout=10):
        """
        关闭首次进入游戏中心时女性弹出框提示
        Args:
            timeout: 查找女性弹出框超时
        Returns:
            True: 关闭陈宫 False: 未找到女性提示框
        """
        # try:
        #     self.device.click_by_id("com.qiyi.gamecenter:id/home_guide_confirm", timeout=timeout)
        #     time.sleep(1)
        #     return True
        # except:
        #     return False
        return self._click_home_woman_known(timeout=timeout)

    def enter_setting(self):
        """
        进入个人中心设置页面
        Returns:
            True: 进入成功
            False：进入失败
         """
        try:
            self.device.click_by_id(self.conf.gamecenter_user.id, timeout=5, desc="点击主页我的图标")
            time.sleep(2)
            self.device.click_by_id(self.conf.gamecenter_user_setting.id, timeout=5, desc="点击设置图标")
            time.sleep(2)
        except Exception as e:
            return False
        return True

    def goto_rank(self):
        """
        进入榜单页
        Returns:
            True: 进入成功， False: 进入失败
        """
        return self.device.click_textview_text("榜单", timeout=10)

    def goto_classify(self):
        """
        进入分类页
        Returns:
            True: 进入成功， False: 进入失败
        """
        return self.device.click_textview_text("分类", timeout=10)

    def into_my_info(self):
        """
        进入个人中心
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            self.device.click_by_id(self.conf.gamecenter_user.id, desc="点击用户图标", timeout=5)
            time.sleep(3)
            return True
        except:
            return False

    def check_woman_ui(self):
        """
        检测女生版游戏中心UI
        Returns:
            True: 检测成功
            False: 检测失败
        """
        title_list = ['精品游戏', '最新游戏']
        for title in title_list:
            title_xpath = self.conf.template_title_tv.xpath.format(title)
            try:
                self.device.swipe_down_find_ele(xpath=title_xpath, timeout=30)
            except:
                g_logger.warning("查找标题：{}失败".format(title))
                return False

        return True


