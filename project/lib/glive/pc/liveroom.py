# -*- coding: UTF-8 -*-

"""
File Name:      liveroom
Author:         zhangwei04
Create Date:    2019/7/23
"""

import os
import time
import re
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.glive.pc.common import Common
from framework.utils.selenium.action_chains import ActionChains
import contextlib

GIFT_BATCH = (1, 10, 33, 66, 520, 1314)     # 礼物批量赠送字典


class LiveRoom(Common):
    """直播间"""
    def __init__(self, target, ele_conf_name='pc'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
        self.recharge_flag = False
        self._is_expense_right = False
        self.get_welfare_rooms = dict()

    def url_into_room(self, room_id, check_chat_ready=False, reload=True):
        """
        通过url进入直播间
        Args:
            room_id: 直播间号
            reload: 若当前url是此直播间url, 是否重新加载
        Returns:
            True: 进入成功, False: 进入失败
        """
        self.device.switch_to_last_window()
        room_url = self.conf.url.room.format(room_id)
        if not reload:
            if self.device.current_url == room_url:
                return True
        self.device.get(room_url)
        try:    # 检测首页弹窗
            self.device.find_element_by_xpath("//div[@class='_ok lottery-close']", timeout=2).click()
            time.sleep(0.5)
            self.close_recommend_tips()
        except:
            pass
        self.get_fans_daily_welfare()

        if check_chat_ready:
            if not self.check_chat_ready():
                return False

        return True

    def check_chat_ready(self, timeout=30):
        """
        检测聊天室准备好
        Returns:
        """
        g_logger.info("检测聊天室是否准备好")
        time_start = time.time()
        while timeout > time.time() - time_start:
            try:
                self.device.find_element_by_xpath(self.conf.room_chat_grey_msg.ready, timeout=1)
                use_time = time.time() - time_start
                if time.time() - time_start > 2:
                    g_logger.warning("直播间弹幕准备时间{}秒, 等待相同时间，确保用户能发言".format(use_time))
                    time.sleep(use_time)
                return g_logger.info("聊天室准备完成")

            except:
                time.sleep(0.3)
        else:
            g_logger.warning("检测聊天室准备完成超时")
            return False

    def check_room_ui(self, classify=None, anchor=None, title=None):
        """
        检查直播间UI
        Args:
            classify: 直播类别，如英雄联盟
            anchor: 主播名称
            title: 直播间标题
        Returns:
            True: 检测成功, False: 检测失败
        """
        if not self.device.check_ele_text_by_id(self.conf.live_room.classify_id, classify, desc="直播间二级分类"):
            return False
        if not self.device.check_ele_text_by_xpath(self.conf.live_room.anchor_xpath, anchor, desc="直播间主播名"):
            return False
        if not self.device.check_ele_text_by_xpath(self.conf.live_room.title_xpath, title, desc="直播间标题"):
            return False
        return True

    def click_gift_bag(self):
        """
        点击礼包按钮
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_by_id(self.conf.room.gift_bag_id, timeout=5, desc="背包")

    def click_charge(self):
        """
        点击充值按钮
        Returns:
            True: 点击成功, False:点击失败
        """
        return self.device.click_by_xpath(self.conf.room.charge, timeout=5, time_sleep=2, desc='充值按钮')

    def bag_send_gift(self, gift_index=None, gift_name=None, count=1, group=None):
        """
        背包赠送礼物，通过礼物位置索引(gift_index)或者礼物名称(gift_name)赠送,
        Args:
            gift_index: 礼物位置，从1开始，若传入此参数，则gift_name不做处理
            gift_name: 礼物名
            count: 赠送礼物数量，
            group: 默认为None，代表非批量赠送；批量赠送时，赠送组数，每组个数是count参数，
        Returns:
            True: 赠送成功, Fasle: 赠送失败
        """
        ele_rst, gift_num, index = self.check_bag_gift_and_get_number(gift_index, gift_name)
        count = int(count)
        if ele_rst:
            if group is None:   # 单个(连续)送
                if int(gift_num) < count:
                    return g_logger.error("要发送的礼物数量{}大于实际礼物数量{}, 请确认".format(count, gift_num))
                for _ in range(count):
                    self.device.click_by_xpath(self.conf.room_bag_gift.gf_item_li.format(index), time_sleep=0.5, timeout=5)
            else:
                group = int(group)
                self.device.move_to_element(ele_rst)
                if gift_num < count * group:
                    return g_logger.error("要发送的礼物数量{}大于实际礼物数量{}, 请确认".format(count * group, gift_num))
                if not self._click_batch_send(count, group):
                    return False
        else:
            return False
        return True

    def _click_batch_send(self, count, group):
        """
        点击批量赠送
        Args:
            count: 每组数量
            group: 赠送组数

        Returns:

        """
        group = int(group)
        # if count not in GIFT_BATCH:
        #     return g_logger.error("每组增送数量{}不在集合{}中".format(count, GIFT_BATCH))
        ele = self.device.get_ele_by_xpath(self.conf.room_gift_batch.count.format(count), timeout=5)
        if ele:
            ele.click()
            time.sleep(2)
        for i in range(group):
            ele1 = self.device.get_ele_by_xpath(self.conf.room_gift_batch.send, timeout=3)
            if ele1:
                g_logger.info("发送第{}组礼物".format(i+1))
                ele1.click()
                time.sleep(2)
            else:
                g_logger.error("查找批量赠送按钮失败")
        time.sleep(1)   # 等待1秒，确保直播间信息刷新
        return True

    def check_chat_gift_info(self, account_section="", gift_name="", gift_num=None, group=None):
        """
        检测聊天室礼物消息信息
        Args:
            account_section: account.conf文件里面的section,如phone_1
            gift_name: 礼物名
            gift_num: 礼物赠送次数
            group: 礼物组数

        Returns:
            True: 检测成功, False: 检测失败
        """
        if account_section:
            if self.account_conf.check_available(account_section):
                user_name = self.account_conf.get(account_section, "desc")
            else:
                return False
        gift_list = self._get_gifts_msg(user_name=user_name, gift_name=gift_name)
        g_logger.info("礼物信息列表：{}".format(gift_list))
        if gift_num and gift_list:
            gift_num = int(gift_num)
            if group:
                group = int(group)
                if group > len(gift_list):
                    return g_logger.error("按组赠送次数不正确，期望{}次，实际捕获房间赠送次数{}".format(group, len(gift_list)))
                send_count = gift_list[-1]['number'] - gift_list[len(gift_list)-group]['number'] if group > 1 else gift_list[-1]['number']
                g_logger.info("期望赠送个数{},实际赠送个数{}".format(group * gift_num, send_count + gift_num))
                return send_count + gift_num == group * gift_num
            else:
                send_count = gift_list[-1]['number'] - gift_list[0]['number'] + 1 if gift_num > 1 else gift_list[-1]['number']
                g_logger.info("期望赠送个数{},实际赠送个数{}".format(send_count, gift_num))
                return send_count >= gift_num
        else:
            return gift_list

    def _get_gifts_msg(self, user_name=None, gift_name=None):
        """
        获取礼物
        Args:
            user_name: 用户名
            gift_name: 礼物道具名
        Returns:
            list: 礼物字典列表,  元素：dict: 礼物信息字典，用户user, 礼物名name, 当前数量number，用户id user_id， 用户等级user_level,
        """
        gift_list = []
        try:
            if user_name and gift_name:
                u_eles = self.device.find_elements_by_xpath(self.conf.room_chat_gift_msg.user_li.format(user_name))
                g_eles = self.device.find_elements_by_xpath(self.conf.room_chat_gift_msg.name_li.format(gift_name))
                eles = [u_ele for u_ele in u_eles for g_ele in g_eles if u_ele == g_ele]
            elif user_name:
                eles = self.device.find_elements_by_xpath(self.conf.room_chat_gift_msg.user_li.format(user_name), timeout=10)
            elif gift_name:
                eles = self.device.find_elements_by_xpath(self.conf.room_chat_gift_msg.name_li.format(gift_name))
            else:
                eles = self.device.find_elements_by_xpath(self.conf.room_chat_gift_msg.li)
        except:
            return g_logger.error("查找聊天信息失败")

        if eles:
            for gift_li_ele in eles:
                gift_list.append(self._format_chat_gift_ele_msg(gift_li_ele))
        return gift_list

    def _format_chat_gift_ele_msg(self, gift_ele):
        """
        格式化聊天室礼物元素信息
        Args:
            gift_ele: 礼物li元素
        Returns:
            dict: 礼物信息字典，用户user, 礼物名name, 当前数量number，用户id user_id， 用户等级user_level
        """
        fmt_d = {"user": None, "user_id": None, "user_level": None, "name": None, "number": None,}
        conf = self.conf.room_chat_gift_msg
        try:
            user_ele = gift_ele.find_element_by_xpath(conf.user)
            fmt_d['user'] = user_ele.text
            fmt_d['user_id'] = user_ele.get_attribute("data-ud")
            fmt_d['user_level'] = user_ele.get_attribute("data-level")
        except:
            g_logger.warning("格式化礼物信息面板，读取用户信息失败")
        try:
            fmt_d['name'] = gift_ele.find_element_by_xpath(conf.name).text
        except:
            g_logger.warning("格式化礼物信息面板，读取名字失败")
        try:
            number = gift_ele.find_element_by_xpath(conf.number).text
            if number:
                number = int(number[1:])
            else:
                number = 1
            fmt_d['number'] = number
        except:
            g_logger.warning("格式化礼物信息面板，读取数量失败")
        return fmt_d

    def check_bag_gift_and_get_number(self, gift_index=None, gift_name=None):
        """
        检测背包礼物并且得到礼物数量
        Args:
            gift_index: 礼物位置，从1开始，若传入此参数，则gift_name不做处理
            gift_name: 礼物名
        Returns:
            check_result: ele: 检测成功,元素实例 False: 检测失败
            gift_num: int: 礼物数量， None: 检测失败时
            index: 元素位置
        """
        if not gift_index and not gift_name:
            return g_logger.error("参数：gift_index, gift_name必须传入一个"), None, None

        one_page_count = 6  # 单页配置的礼物数量
        page_count = len(self.device.find_elements_by_xpath(self.conf.room_bag_gift.pagi_li))
        g_logger.info("背包共有:{}页礼物".format(page_count))

        if gift_index:  # 通过礼物index查找元素
            gift_index = int(gift_index)
            if gift_index > page_count * one_page_count:
                return g_logger.error("index位置：{} 大于当前礼物总数".format(gift_index)), None, None

            while gift_index > one_page_count:  # 滑动到对应页面
                self.device.click_by_xpath(self.conf.room_bag_gift.right, timeout=5, desc="下一页按钮")
                gift_index -= one_page_count

            gift_ele = self.device.get_ele_by_xpath(self.conf.room_bag_gift.gf_item_li.format(gift_index), timeout=5)
            if gift_ele is None:
                return g_logger.error("通过index:{}获取背包礼物元素失败".format(gift_index)), None, None
            return gift_ele, self._get_bag_gift_num(gift_ele), gift_index
        else:
            # 通过礼物名获取礼物元素
            for _ in range(page_count):
                gift_num = None
                for index in range(1, 1 + one_page_count):
                    ele_li = self.device.get_ele_by_xpath(self.conf.room_bag_gift.gf_item_li.format(index), timeout=5)
                    if "empty" in ele_li.get_attribute("class"):
                        gift_num = 0
                        break
                    if ele_li:
                        self.device.move_to_element(ele_li)
                        desc = self._get_gift_msg(only_name=True)
                        if desc['name'] == gift_name:
                            gift_num = self._get_bag_gift_num(ele_li)
                            return ele_li, gift_num, index

                if gift_num == 0:   # 一直找到空礼物位置，中断循环，返回失败
                    break
                # 进入下一页
                self.device.click_by_xpath(self.conf.room_bag_gift.right, timeout=5, desc="下一页按钮")

            return g_logger.error("未找到礼物:{}元素".format(gift_name)), None, None

    def _get_gift_msg(self, only_name=False):
        """
        读取礼物描述
        Args:
            only_name: 是否只查找礼物名标志
        Returns:
            dict: 描述字典，名称'name'， 价格price，贡献值contribute， 经验值experience, 亲密度validity, 礼物类型type(0是奇豆，1是金币)
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_gift.desc_ele, timeout=5)
        item_dict = {'name': None, "price": None, "contribute": None, "experience": None, "validity": None, "type": None}
        if ele is None:
            g_logger.error("查找礼物描述元素失败")
        elif not ele.is_displayed():
            g_logger.error("礼物描述元素未展示出来")
        else:
            try:
                conf = self.conf.room_gift
                item_dict['name'] = ele.find_element_by_xpath(conf.name).text
                if only_name:   # 只查找礼物名，此处直接返回
                    return item_dict
            except:
                g_logger.warning("读取礼物信息面板信息名称失败")
            try:
                price_msg = ele.find_element_by_xpath(conf.price).text
                if "奇豆" in price_msg:
                    item_dict['type'] = 0
                elif "金币" in price_msg:
                    item_dict['type'] = 1
                price_l = re.findall("\d+", price_msg)
                if price_l:
                    item_dict['price'] = int(price_l[-1])
            except:
                g_logger.warning("读取礼物信息面板信息价格失败")
            try:
                item_dict['validity'] = ele.find_element_by_xpath(conf.affinity).text
            except:
                g_logger.warning("读取礼物信息面板信息亲密度失败")
            try:
                contribute_exper = ele.find_element_by_xpath(conf.contribute_exper).text    # 贡献值和经验值在一个元素下
                item_dict['contribute'], item_dict['experience'] = tuple(re.findall("\+(\d+)", contribute_exper))
            except:
                g_logger.warning("读取礼物信息面板信息贡献值、经验值失败")
        return item_dict

    def _get_bag_gift_num(self, gift_ele):
        """
        获取背包礼物数量
        Args:
            gift_ele: 背包礼物元素
        Returns:
            int: 背包礼物数量
        """
        try:
            if 'empty' in gift_ele.get_attribute("class"):
                return 0
            ele = gift_ele.find_element_by_xpath(self.conf.room_bag_gift.gf_item_num)
            return int(ele.text)
        except:
            return 1

    def close_first_recharge(self, account_section, timeout=65):
        """
        点掉6折优惠弹窗
        Returns:
            True: 点击成功, False: 点击失败
        """
        if self.account_conf.check_available(account_section):
            recharged = self.account_conf.get(account_section, "recharged")
            if int(recharged):
                return True
        else:
            return False

        time_start = time.time()
        while timeout > time.time() - time_start:
            try:
                ele = self.device.find_element_by_xpath(self.conf.first_recharge.close, timeout=3)
                if ele.is_displayed():
                    ele.click()
                    time.sleep(0.5)
                    return True
            except Exception as e:
                time.sleep(1)
        else:
            return g_logger.error("查找6折优惠弹窗超时")

    def check_follow(self):
        """
        检测直播间是否已经关注
        Returns:
            True: 已关注， False: 未关注
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_follow.btn, timeout=5)
        if ele:
            text = ele.text
            if text == "关注":
                return False
            elif text == "已关注":
                return True
            else:
                return None
        else:
            return None

    def _get_follow_number(self):
        """
        获取关注人数
        Returns:
            int: 关注人数, None:获取失败
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_follow.count)
        return int(ele.text) if ele else -1

    def follow(self):
        """
        关注直播
        Returns:
            True: 关注成功, False: 关注失败
        """
        check_rst = self.check_follow()
        if check_rst is None:
            return g_logger.error("获取关注文本失败")
        if check_rst:
            return g_logger.info("用户已关注，不做操作")
        follow_num = self._get_follow_number()
        g_logger.info("关注前，关注人数: {}".format(follow_num))

        if not self.device.click_by_xpath(self.conf.room_follow.btn, timeout=5, desc="关注按钮"):
            return g_logger.error("查找关注按钮失败")

        followed_num = self._get_follow_number()
        g_logger.info("关注后，关注人数: {}".format(followed_num))
        return self.check_follow() is True and followed_num - follow_num == 1

    def unfollow(self):
        """
        取消关注
        Returns:
            True: 取消chen成功, False: 取消失败
        """
        check_rst = self.check_follow()
        if check_rst is None:
            return g_logger.error("获取关注文本失败")
        if not check_rst:
            return g_logger.info("用户未关注，不做操作")

        follow_num = self._get_follow_number()
        g_logger.info("取消关注前，关注人数: {}".format(follow_num))
        if self.device.click_by_xpath(self.conf.room_follow.btn, timeout=5, desc="已关注按钮"):
            if not self.device.click_by_xpath(self.conf.room_follow.un_ensure, timeout=5, desc="确认按钮"):
                return g_logger.error("查找确认按钮失败")
        else:
            return g_logger.error("查找关注按钮失败")

        followed_num = self._get_follow_number()
        g_logger.info("取消关注后，关注人数: {}".format(followed_num))
        return self.check_follow() is False and followed_num - follow_num == -1

    def _open_emoji_bag(self):
        """
        打开表情背包
        Returns:
            True: 打开成功, False: 打开失败
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_chat_emoji.popover)
        if ele and ele.is_displayed():
            return g_logger.info("表情背包已经打开，不做操作")

        return self.device.click_by_id(self.conf.room_chat_send_box.emoji_id)

    def _click_emoji_in_bag(self, emoji):
        """
        点击背包表情
        Args:
            emoji: 表情数据,

        Returns:
            True: 点击成功, False: 点击失败
        """
        if not self._open_emoji_bag():
            return g_logger.error("打开表情背包失败")
        if isinstance(emoji, str):
            emoji = [emoji]
        elif not isinstance(emoji, (list, tuple)):
            return g_logger.error("emoji参数不正确，需要是str或者list,tuple")
        for em in emoji:
            try:
                ele = self.device.find_element_by_xpath(self.conf.room_chat_emoji.li.format(em))
                pos = ele.location_once_scrolled_into_view
                self.device.find_element_by_xpath(self.conf.room_chat_emoji.li.format(em)).click()
            except:
                return g_logger.error("查找表情包表情元素：{}失败".format(em))
        return True

    def click_chat_send_button(self, time_sleep=1):
        """
        点击聊天室发送按钮
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_by_xpath(self.conf.room_chat_send_box.send_button, time_sleep=time_sleep)

    def _format_chat_text_msg(self, li_ele):
        """
        格式化聊天室文本信息（包含表情）
        Args:
            li_ele: 聊天室单条信息元素
        Returns:
            dict: 格式化后的信息字典，包含：用户名名user，文本内容content，表情列表emoji, 用户ID user_id, 用户等级user_level
        """
        fmt_d = {'user':None, 'user_id': None, 'user_level': None, 'emoji':[]}
        conf = self.conf.room_chat_text_msg
        try:
            user_ele = li_ele.find_element_by_xpath(conf.user)
            fmt_d['user'] = user_ele.text
            fmt_d['user_id'] = user_ele.get_attribute("data-ud")
            fmt_d['user_level'] = user_ele.get_attribute("data-level")
            fmt_d['content'] = li_ele.find_element_by_xpath(conf.content).text[1:]  # 第一个是':'，不需要
            emoji_eles = li_ele.find_elements_by_xpath(conf.emoji)
            if emoji_eles:
                fmt_d['emoji'] = [ele.get_attribute('src').rsplit("/", 1)[1].split(".")[0] for ele in emoji_eles]
        except Exception as e:
            g_logger.warning(str(e))
            g_logger.warning("读取聊天框礼物元素部分信息失败")
        return fmt_d

    def chat_send_msg(self, text="", emoji=[], time_sleep=1):
        """
        聊天室发送聊天信息
        Args:
            text: 聊天文本信息
            emoji: 表情列表
            time_sleep: 点击发送后，等待时间
        Returns:
            True:输出成功, False: 输入失败
        """
        if not self.chat_input_msg(text=text, emoji=emoji):
            return False
        return self.device.click_by_xpath(self.conf.room_chat_send_box.send_button, time_sleep=time_sleep)

    def chat_input_msg(self, text="", emoji=[]):
        """
        聊天室输入聊天信息
        Args:
            text: 聊天文本
            emoji: 表情列表
        Returns:
            True: 输入成功， False: 输入失败
        """
        if text:
            ele = self.device.get_ele_by_id(self.conf.room_chat_send_box.send_message_id)
            if ele:
                if not ele.is_displayed():
                    return g_logger.error("发送文本框未展示")
                # try:
                #     ele.click()
                #     time.sleep(0.5)
                # except:
                #     pass
                try:
                    ele.clear()
                except Exception as e:
                    ele = self.device.get_ele_by_id(self.conf.room_chat_send_box.send_message_id)
                    if not ele:
                        return g_logger.error("清空发送文本失败")
                    ele.clear()

                ele.send_keys(text)
            else:
                return g_logger.error("查找发送文本失败")
        if emoji:
            return self._click_emoji_in_bag(emoji)
        return True

    def get_chat_send_msg(self):
        """
        读取待发送信息
        Returns:
            str: 待发送信息
        """
        ele = self.device.get_ele_by_id(self.conf.room_chat_send_box.send_message_id)
        if not ele:
            return g_logger.error("读取待发送信息失败")
        return ele.text

    def check_chat_text_msg(self, text="", user=None, user_section=None, emoji=[], timeout=5):
        """
        检测聊天室文本信息，包含表情
        Args:
            text: 直播间文本，需要是连续的，不包括表情的，如“text1[e]text2”需要改成text1text2，表情在emoji里设置
            user: 用户名，若使用此参数，则user_section参数失效
            user_section:用户session，需要在account.conf文件里配置的用户session，如‘phone_1’
            emoji: 表情列表，如['e', 'bs', 'bs']
        Returns:
            True: 检测成功, False:检测失败
        """
        user = user
        # user_uid = None
        if emoji and isinstance(emoji, str):
            emoji = [emoji]

        if not user and user_section:
            if self.account_conf.check_available(user_section):
                user = self.account_conf.get(user_section, "desc")
                # user_uid = self.account_conf.get(user_section, "uid")
            else:
                return g_logger.error("查找账户配置文件section:{}失败".format(user_section))
        time_start = time.time()
        while time.time() - time_start < timeout:
            li_eles = self.device.find_elements_by_xpath(self.conf.room_chat_text_msg.li, timeout=1)
            if li_eles:
                break
        else:
            return g_logger.error("直播间没有用户发言")

        text_msg_info = [self._format_chat_text_msg(li_ele) for li_ele in li_eles]
        g_logger.info("直播间用户发言信息：{}".format(text_msg_info))
        for msg in reversed(text_msg_info):     # 从后往前找
            # g_logger.info("    用户：{user}, 内容:{content}, 表情：{emoji}".format(**text))
            if user and user != msg['user']:
                continue
            if text and emoji:
                if text in msg['content'] and emoji == msg['emoji']:
                    return True
            elif text:
                if text in msg['content']:
                    return g_logger.info("聊天室文本：{}".format(msg['content']))
            elif emoji:
                if emoji == msg['emoji']:
                    return g_logger.info("表情列表：{}".format(msg['emoji']))
        else:
            return g_logger.error("聊天室信息匹配失败")

    def chat_clean_msg(self):
        """
        直播间清除消息
        Returns:
            True: 清除成功, False: 清除失败
        """
        return self.device.click_by_id(self.conf.room_chat_send_box.clear_id)

    def check_chat_msg_cleaned(self):
        """
        通过查找直播间信息列表第一个元素，检测直播间消息已经被清除过
        Returns:
            True: 检测成功, False: 检测失败
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_chat.li)
        if ele:
            cls = ele.get_attribute("class")
            g_logger.info("聊天室第一条文本信息：{}".format(ele.text))
            return cls == "orange"
        else:
            return g_logger.error("查找直播间聊天室li元素失败")

    @contextlib.contextmanager
    def _expense_record(self, type, price, count=1, group=None):
        """
        计算花费函数
        Args:
            type: 消耗类型，0奇豆,1金币
            price: 礼物价格
            count: 赠送礼物数量，默认送1个, 若批量增送为True(对应batch参数)，则此参数值需要在GIFT_BATCH中
            group: 批量赠送时，赠送组数，每组个数是count参数，

        Yields:
            bool: True:余额充足, False:余额不足
        """
        get_num_fn = self._get_qidou_num if type == 0 else self._get_gold_num
        expense = int(price) * int(count) if group is None else int(price) * int(count) * int(group)
        self._is_expense_right = False
        pre_num = get_num_fn()
        ret = pre_num >= expense
        yield ret
        # 确认花费情况
        time.sleep(1)   # 延时1秒，确保金额刷新
        cur_num = get_num_fn()
        acutal_expense = pre_num - cur_num
        g_logger.info("当前余额：{} 期望消耗：{}, 实际消耗：{}".format(cur_num, expense, acutal_expense))
        self._is_expense_right = acutal_expense == expense

    def send_gift(self, gift_index=None, gift_name=None, count=1, group=None):
        """
        赠送礼物，通过礼物位置索引(gift_index)或者礼物名称(gift_name)赠送,
        Args:
            gift_index: 礼物位置，从1开始，若传入此参数，则gift_name不做处理
            gift_name: 礼物名
            count: 赠送礼物数量，默认送1个, 若批量增送为True(对应batch参数)，则此参数值需要在GIFT_BATCH中
            group: 批量赠送时，赠送组数，每组个数是count参数，
        Returns:
            True: 赠送成功, Fasle: 赠送失败
        """
        count = int(count)
        # 礼物元素查找流程
        if not gift_index and not gift_name:
            return g_logger.error("参数：gift_index, gift_name需要传入一个")
        elif not gift_index:
            # 读取礼物道具名，获取礼物元素
            eles_li = self.device.find_elements_by_xpath(self.conf.room_gift_list.li)
            for index, gift_ele in enumerate(eles_li):
                gift_index = index + 1
                if not gift_ele.is_displayed():
                    gift_ele.location_once_scrolled_into_view
                gift_ele = self.device.get_ele_by_xpath(self.conf.room_gift_list.li_index.format(gift_index))

                self.device.move_to_element(gift_ele)
                gift_info = self._get_gift_msg()
                if gift_info['name'] == gift_name:
                    break
            else:
                return g_logger.error("通过礼物名:{}获取礼物index失败".format(gift_name))
        else:
            # 通过index查找礼物元素
            gift_ele = self.device.get_ele_by_xpath(self.conf.room_gift_list.li_index.format(gift_index))
            if not gift_ele:
                return g_logger.error("通过index查找礼物元素失败")
            if not gift_ele.is_displayed():
                gift_ele.location_once_scrolled_into_view
            # 元素位置变动，从新查找
            gift_ele = self.device.get_ele_by_xpath(self.conf.room_gift_list.li_index.format(gift_index))
            self.device.move_to_element(gift_ele)
            gift_info = self._get_gift_msg()     # 读取礼物信息

        # 通过礼物信息弹窗读取礼物价格和类型及账户对应类型的数量
        g_logger.info("礼物信息：{}".format(gift_info))
        if not gift_info['price']:
            return g_logger.error("获取礼物价格失败")
        if gift_info['type'] is None:
            return g_logger.error("获取礼物类型失败")

        # 礼物赠送流程
        with self._expense_record(gift_info['type'], gift_info['price'], count=count, group=group) as is_enough:
            if not is_enough:
                return g_logger.error("账户金额不足")

            if group is not None:   # 批量赠送
                group = int(group)
                if not self._click_batch_send(count, group):
                    return False
            else:   # 单击礼物图片赠送
                for _ in range(count):
                    try:
                        gift_ele.click()
                    except:
                        return g_logger.error("找到礼物图片，点击产生异常")
                    time.sleep(1)

        if not self._is_expense_right:
            return g_logger.error("消耗数量不正确")

        return True

    def _get_qidou_num(self):
        """
        获取奇豆数量
        Returns:
            int：奇豆数量
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_wallet.beans, timeout=5)
        if not ele:
            g_logger.error("获取奇豆元素失败")
            return None
        else:
            return int(ele.text)
    
    def _get_gold_num(self):
        """
        获取奇豆数量
        Returns:
            int：奇豆数量
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_wallet.gold, timeout=5)
        if not ele:
            g_logger.error("获取金币元素失败")
            return None
        else:
            return int(ele.text)

    def get_chat_gift_cards_msg(self):
        """
        获取聊天室弹窗礼物卡片信息
        Returns:
            list: 礼物信息列表，元素为字典，
        """
        gift_card_eles = self.device.find_elements_by_xpath(self.conf.room_chat_gift_card.li)
        if not gift_card_eles:
            return []
        else:
            return [self._format_chat_gift_card_msg(li_ele) for li_ele in gift_card_eles]

    def _format_chat_gift_card_msg(self, li_ele):
        """
        格式化直播间礼物卡信息
        Args:
            li_ele: 卡片元素实例
        Returns:
            dict: 格式化信息字典，用户名user, 礼物名gift_name, 礼物图片名gift_img, 连击数量number
        """
        card_msg = {"user": None, "gift_name":None, "img_name": None, "number": None}
        conf = self.conf.room_chat_gift_card
        try:
            card_msg['user'] = li_ele.find_element_by_xpath(conf.user_name).text
        except:
            g_logger.warning("直播间礼物卡片信息获取：用户名失败")
        try:
            card_msg['gift_name'] = li_ele.find_element_by_xpath(conf.gift_name).text[2:]
        except:
            g_logger.warning("直播间礼物卡片信息获取：礼物名失败")
        try:
             ele = li_ele.find_element_by_xpath(conf.img_gift)
             img_path = ele.get_attribute("src")
             card_msg['img_name'] = re.findall("/(\w+)\.png", img_path)
        except:
            g_logger.warning("直播间礼物卡片信息获取：礼物图片名失败")
        try:
            card_msg['number'] = int(li_ele.find_element_by_xpath(conf.num).text)
        except:
            g_logger.warning("直播间礼物卡片信息获取：礼物图片名失败")
        return card_msg

    def check_user_ban(self, text="123", user_section=None):
        """
        检测当前用户是否被禁言，预置条件：已有用户登录
        Args:
            text: 试探禁言的发送消息
            user_section: 用户登录session
        Returns:
            True: 用户被禁言, False: 未被禁言, None: 检测失败
        """

        if user_section:
            if not self.target.Login.password_login(account_section=user_section):
                return False
        self.chat_clean_msg()   # 先清除消息
        self.device.click_by_xpath(self.conf.room_chat_msg_track.close, timeout=2)
        if not self.chat_send_msg(text=text, time_sleep=0.5):
            g_logger.error("用户发送消息失败")
            return None
        time_start = time.time()
        while time.time() - time_start < 3:
            try:
                if self.device.find_element_by_xpath(self.conf.room_chat_toast.ban, timeout=0.2).is_displayed():
                    return True
            except Exception as e:
                pass
        return False

    def ban_user(self, user_section, target):
        """
        在当前直播间对用户禁言
        Args:
            target: 辅助用户Taget对象
        Returns:
            True: 禁言成功, False: 禁言失败
        """
        text = "auto ban"
        is_ban = target.LiveRoom.check_user_ban(text=text)
        if is_ban:
            return g_logger.info("用户已经被禁言")
        elif is_ban is None:
            target.device.get_screenshot_as_file(
                os.path.join(g_resource['testcase_log_dir'], "{}_check_user_ban_{}_failed.png".format(target.name, g_resource['testcase_loop'])))
            return g_logger.error("检测用户是否被禁言失败")
        else:
            g_logger.info("用户未被禁言,开始禁言用户")
            if self._click_chat_user_ban(uid=self.account_conf.get(user_section, "uid")):
                return g_logger.info("点击禁言按钮成功")
            else:
                target.device.get_screenshot_as_file(
                    os.path.join(g_resource['testcase_log_dir'], "{}_check_user_ban_{}_failed.png".format(target.name, g_resource['testcase_loop'])))
                return g_logger.error("点击用户禁言按钮失败")

    def _click_chat_user_ban(self, user_name=None, uid=None):
        """
        点击直播间用户禁言
        Args:
            user_name: 用户名
            uid: 用户UID
        Returns:
            True: 点击成功, False: 点击失败
        """
        if user_name:
            find_xpath = self.conf.room_chat_text_msg.user_name_text_f.format(user_name)
        elif uid:
            find_xpath = self.conf.room_chat_text_msg.user_name_uid_f.format(uid)
        else:
            return g_logger.error("参数user_name, uid 必须传入一个")
        # 聊天室查找用户名元素，并点击
        user_ele = self.device.get_ele_by_xpath(find_xpath, timeout=5)
        if not user_ele:
            return g_logger.error("聊天室查找用户元素失败")
        try:
            user_ele.click()
        except Exception as e:
            self.device.tap_ele_by_position(user_ele, time_sleep=1)   # 元素直接click会抛异常
        time.sleep(7)
        # 点击用户信息窗的禁言元素
        ret = True
        try:
            ban_ele = self.device.find_element_by_xpath(self.conf.room_chat_user_noble_card.mute_user)
            ban_ele.click()
            time.sleep(0.5)
        except Exception as e:
            ban_ele = self.device.find_element_by_xpath(self.conf.room_chat_user_noble_card.mute_user)
            g_logger.error("聊天室通过用户名元素查找禁言元素失败, 请确实此用户是否是管理员")
            ret = False

        # 检测禁言消息弹窗是否出现
        # chat_toast_ele = self.device.get_ele_by_xpath(self.conf.room_chat_toast.ban, timeout=2)
        # if chat_toast_ele:
        #     ret = "已被禁言" in chat_toast_ele.text
        # else:
        #     ret = False
        #     g_logger.error("直播间查找禁言弹窗信息失败")
        # self.device.click_by_xpath(self.conf.room_chat_user_noble_card.close, "关闭弹窗")
        return ret

    def check_not_live(self):
        """
        检测主播没有开播状态
        Returns:
            True: 检测成功， False:检测失败
        """
        status_ele = self.device.get_ele_by_xpath(self.conf.room_not_live.status, timeout=3)
        if not status_ele or status_ele.text != "主播不在家，先看看别的主播吧":
            return g_logger.error("主播不在直播，查找状态失败")
        else:
            g_logger.info("直播状态信息：{}".format(status_ele.text))
        time_ele = self.device.get_ele_by_xpath(self.conf.room_not_live.time, timeout=3)
        if not time_ele:
            return g_logger.error("主播不在直播，查找上次直播时间失败")
        else:
            g_logger.info("上次直播时间: {}".format(time_ele.text))
        return True

    def check_fans_daily_window(self, timeout=2):
        """
        检测粉丝每日福利弹窗
        Returns:
            True: 检测到弹窗, False: 未检测到弹窗
        """
        return self.device.get_ele_by_xpath(self.conf.room_fans_daily_welfare.gift_a, timeout=timeout)

    def close_fans_daily_window(self, timeout=2):
        """
        关闭粉丝每日福利弹窗
        Returns:
            True: 检测到弹窗, False: 未检测到弹窗
        """
        self.device.close_by_xpath(self.conf.room_fans_daily_welfare.close, timeout=timeout)

    def get_fans_daily_welfare(self):
        """
        领取粉丝每日福利
        Returns:
            True: 领取成功, False:领取失败
        """
        if not self.device.click_by_xpath(self.conf.room_fans_daily_welfare.gift_a, timeout=2):
            return False
        else:
            g_logger.info("点击领取每日礼物按钮成功")
        conf = self.conf.room_fans_daily_welfare_get
        ele = self.device.get_ele_by_xpath(conf.modal)
        if not ele:
            return g_logger.error("读取领取每日福利成功弹窗失败")
        try:
            g_logger.info("标题：{}".format(ele.find_element_by_xpath(conf.title).text))
            g_logger.info("礼物名：{}".format(ele.find_element_by_xpath(conf.gift_name).text))
            g_logger.info("礼物描述：{}".format(ele.find_element_by_xpath(conf.gift_desc).text))
        except:
            pass
        try:
            ele.find_element_by_xpath(conf.gift_now).click()
            time.sleep(1)
            return True
        except:
            return g_logger.error("查找'知道了'按钮失败")

    # 抽奖相关
    def check_lottery_status(self, status):
        """
        Args:
            status: 开奖状态，取值范围：未中奖，开奖中，已中奖，未开奖
        检测直播间是否正在抽奖
        Returns:
            True: 检测成功, False: 检测失败
        """
        return status == self.get_lottery_status()

    def get_lottery_status(self):
        """
        Args:
        读取直播间抽奖状态
        Returns:
            True: 正在抽奖, False: 没有抽奖
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_games_list.lottery_status)
        if not ele:
            return g_logger.error("查找抽奖状态按钮失败")
        text = ele.text
        g_logger.info("当前抽奖状态: {}".format(text))
        if ele.is_displayed():
            return text
        else:
            return "未开奖"

    def click_lottery(self):
        """
        点击抽奖图标，若正在开奖，则弹出开奖任务弹窗；若已中奖，则弹出已中奖弹窗；若未中奖，则弹出主播未开奖或者未中奖弹窗
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_by_xpath(self.conf.room_games_list.lottery_img, desc="抽奖图像", timeout=2)

    def is_drawn_lottery(self):
        """
        检测是否正在抽奖
        Returns:
            True: 正在抽奖, False: 否
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_lottery_box.popover)
        if ele:
            return ele.is_displayed()
        return False

    def do_follow_task(self):
        """
        做关注主播任务
        Returns:
            True: 任务成功, False: 任务失败
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_lottery_box.task_li)
        if ele:
            try:
                self.device.find_element_by_xpath(self.conf.room_lottery_box.task_follow).click()
                time.sleep(2)
            except:
                return g_logger.error("查找'关注'关键字失败")
        else:
            return g_logger.error("查找任务li失败")

        ele = self.device.get_ele_by_xpath(self.conf.room_lottery_box.task_follow_status)
        if ele:
            g_logger.info("做完'关注'任务状态：{}".format(ele.text))
            return ele.text == "已完成"
        else:
            return g_logger.error("查找'关注'任务状态失败")

    def do_copy_word_task(self, word, timeout=30):
        """
        做复制口令任务
        Returns:
            True: 任务成功, False: 任务失败
        """
        ele = self.device.get_ele_by_xpath(self.conf.room_lottery_box.task_li)
        if ele:
            try:
                self.device.find_element_by_xpath(self.conf.room_lottery_box.task_copy_word).click()
                time.sleep(1)
            except Exception as e:
                if not self._get_copy_word_task_status(word):
                    return g_logger.error("查找'立即复制'关键字失败,且任务不是已完成")
                else:
                    return g_logger.info("任务已经是完成状态")
            else:
                g_logger.error("检测发送框口令:{}".format(self.get_chat_send_msg()))
                time_start = time.time()
                while timeout > time.time() - time_start:
                    self.click_chat_send_button(time_sleep=2)
                    ele = self.device.get_ele_by_xpath(self.conf.room_chat_toast.danmu_prepare, timeout=1)
                    if not ele:
                        break
                else:
                    return g_logger.error("弹幕还在准备,发送口令超时")

                return self._get_copy_word_task_status(word)
        else:
            return g_logger.error("查找任务li失败")

    def _get_copy_word_task_status(self, word):
        for i in range(2):
            ele = self.device.get_ele_by_xpath(self.conf.room_lottery_box.task_copy_word_status.format(word))
            if ele:
                g_logger.info("复制口令任务状态：{}".format(ele.text))
                return ele.text == "已完成"
            else:
                g_logger.warning("检测抽奖任务状态失败，可能是抽奖页面被隐藏，尝试点击抽奖图标调起抽奖页")
                self.device.click_by_xpath(self.conf.room_games_list.lottery_img, desc="抽奖图标", timeout=2)
        else:
            return g_logger.error("查找'复制任务失败'任务状态失败")

    def wait_for_lottery_end(self):
        """
        等待抽奖结束
        Returns:
            True: 执行成功, False: 执行失败
        """
        time.sleep(2)   # 等待2秒，确保页面时间刷新
        time_end = self._get_lottery_time()
        if time_end:
            g_logger.info("等待{}秒，抽奖结束".format(time_end + 2))
            time.sleep(time_end + 2)
            return True
        else:
            return False

    def _get_lottery_time(self, timeout=5):
        """
        读取抽奖剩余时间
        Returns:
            int：距离抽奖结束时间，单位秒，None: 获取时间失败
        """
        g_logger.info("读取抽奖时间")
        time_start = time.time()
        times = []
        while timeout > time.time() - time_start:
            try:
                times = [ele.text for ele in self.device.find_elements_by_xpath(self.conf.room_lottery_box.clock_nums)]
            except:
                self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'],
                        "读取抽检时间异常_{}.png".format(time.strftime("%Hh-%Mm-%Ss", time.localtime()))))
                g_logger.warning("读取抽奖时间异常")
            if not times:
                time.sleep(0.3)
                continue
            try:
                mins = int("".join(times[:2]))
                snds = int("".join(times[2:]))
                return mins * 60 + snds
            except Exception as e:
                g_logger.error("格式化抽奖时间失败")
                g_logger.warning(str(e))
                return None
        else:
            g_logger.warning("未找到抽奖时间")
            return None

    def check_lottery_win_ui(self, timeout=60):
        """
        检测中奖页面
        Returns:
            True: 检测成功, False: 检测失败
        """
        conf = self.conf.room_lottery_win
        time_start = time.perf_counter()
        # self.device.refresh()
        while timeout > time.perf_counter() - time_start:
            ele = self.device.get_ele_by_xpath(conf.modal, timeout=2)
            if not ele:
                return g_logger.error("查找中奖弹窗失败")
            elif ele.is_displayed():
                break
            else:
                g_logger.info("直播弹窗未弹出来，继续检测")
                time.sleep(2)
        else:
            return g_logger.error("中奖弹窗未弹出，未中奖")

        try:
            g_logger.info("中奖标题：{}".format(ele.find_element_by_xpath(conf.tittle).text))
            g_logger.info("奖品名称：{}".format(ele.find_element_by_xpath(conf.prize_name).text))
            # g_logger.info("联系方式：{}".format(ele.find_element_by_xpath(conf.write_address).text))
        except:
            return g_logger.error("查找中奖信息失败")
        return True

    def check_all_task_done(self):
        """
        检测所有任务均已完成
        Returns:
            True: 检测成功, False: 检测失败
        """
        eles = self.device.find_elements_by_xpath(self.conf.room_lottery_box.task_li)
        try:
            tasks_status = [ele.find_element_by_xpath(self.conf.room_lottery_box.task_status).text for ele in eles]
            g_logger.info("任务完成状态：{}".format(tasks_status))
            for i, task_status in enumerate(tasks_status):
                if task_status != "已完成":
                    g_logger.error("任务{}未完成".format(i+1))
                    return False
            else:
                return True
        except Exception as e:
            return g_logger.error("读取任务状态失败")

    def close_lottery_box(self):
        """
        关闭抽奖弹窗
        Returns:
            True: 关闭成功, False:关闭失败
        """
        return self.device.click_by_xpath(self.conf.room_lottery_box.close, timeout=2)
