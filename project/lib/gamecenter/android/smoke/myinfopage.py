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


class GameButtonStatus:
    """游戏按钮状态"""
    install = "install"
    open = "open"
    download = "download"
    click_play = "click_play"
    descs = {"install": "安装", "open": "打开", "download":"下载", "click_play": "点击即玩"}

    @classmethod
    def get_desc(cls, status):
        return cls.descs.get(status)


class MyInfoPage(Common):
    """个人中心页面"""

    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
        self.last_env = None

    def check_ui(self):
        """
        检测个人中心UI布局
        Returns:
            True: 检测成功, False: 检测失败
        """
        try:
            self.device.find_element_by_xpath(self.conf.comment_title.xpath.format("个人中心"), timeout=10)
        except:
            g_logger.error("查找标题:个人中心 失败")
            return False
        eles = self.device.find_elements_by_xpath(self.conf.my_info_tab.xpath_names)
        if eles:
            tab_names = {ele.get_attribute("text") for ele in eles}
            tab_expect = {"玩过", "小游戏", "已预约"}
            g_logger.info("查找到的标签：\n\t{}".format("\n\t".join(tab_names)))
            return tab_expect.issubset(tab_names)
        else:
            g_logger.error("获取标签名失败")
            return False

    def check_default_tab_ui(self, tab_name='玩过', game_name=None, timeout=240):
        """
        检测默认tab UI
        Args:
            tab_name: 标签名
            game_name: 游戏(列表)名
            timeout: 超时
        Returns:
            True: 检测成功, False: 检测失败
        """
        time.sleep(3)
        return self.check_tab_ui(tab_name=tab_name, game_name=game_name, timeout=timeout)

    def click_tab(self, tab_name):
        """
        点击标签
        Args:
            tab_name: 标签名
        Returns:
            True: 执行点击标签操作，False: 未找到标签
        """
        tab_xpath = self.conf.my_info_tab.xpath_name.format(tab_name)
        try:
            self.device.click_by_xpath(tab_xpath, timeout=10)
            time.sleep(3)
            return True
        except:
            g_logger.error("点击标签：{}失败".format(tab_name))
            return False

    def check_tab_ui(self, tab_name, game_name=None, timeout=240):
        """
        检测Tab UI
        Args:
            tab_name: 标签名
            game_name: 游戏名
            timeout: 超时
        Returns:
            True: 检测成功, False: 检测失败
        """
        tab_num = self._get_check_tab_num(tab_name)
        g_logger.info("标签{}的个数为：{}".format(tab_name, tab_num))
        try:
            tab_num = int(tab_num)
        except:
            g_logger.error("标签个数不是数字")
            self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], 'int_tab_num_error.png'))
            return False

        if int(tab_num) > 0:
            game_items_xpath = "//android.widget.TextView[@resource-id='com.qiyi.gamecenter:id/vertical_game_item_name']"
            found_game_list = self._get_all_game_from_vertical_game(eles_xpath=game_items_xpath, timeout=timeout)
            g_logger.info("实际游戏列表个数： {}".format(len(found_game_list)))
            g_logger.info("实际游戏里列表：{}".format(", ".join(found_game_list)))
            return len(found_game_list) == int(tab_num)
        else:
            try:
                ele = self.device.find_element_by_id(self.conf.tv_empty_prompt.id, timeout=10)
                g_logger.info(ele.get_attribute("text"))
                return True
            except:
                g_logger.error("查找标签数量为空时，描述失败")
                return False
        # 改成上面的检测方式
        # if game_name:
        #     game_name_list = [game_name] if isinstance(game_name, str) else list(game_name)
        #     game_items_xpath = "//android.widget.TextView[@resource-id='com.qiyi.gamecenter:id/vertical_game_item_name']"
        #
        #     found_game_list = self._get_all_game_from_vertical_game(eles_xpath=game_items_xpath, timeout=timeout)
        #     # found_game_list = self._get_games_from_vertical_game(game_name_list, eles_xpath=game_items_xpath, timeout=timeout)
        #     # g_logger.info("期望游戏里列表：{}".format(", ".join(game_name_list)))
        #     g_logger.info("实际游戏里列表：{}".format(", ".join(found_game_list)))
        #     if not set(game_name_list).issubset(set(found_game_list)):
        #         return False
        #
        # return True

    def goto_game_detail(self):
        """
        进入游戏详情页
        Returns:

        """
        pass

    def _get_check_tab_num(self, tab_name):
        """
        检测Tab
        Args:
            tab_name: 获取标签右侧游戏的数量
        Returns:
            int: 标签数量
        """
        try:
            ele = self.device.find_element_by_xpath(self.conf.my_info_tab.xpath_num.format(tab_name), timeout=10)
            return ele.get_attribute("text")
        except:
            g_logger.warning("未找到标签：{}的个数, 返回0".format(tab_name))
            return 0

    def switch_environment(self, env=None, read_env=True):
        """切换环境变量. 切换优先级：环境变量配置 > 参数配置 > 默认(线上环境)
        Args:
            env: 取值online、pre_release、test
            read_env: 是否读取环境变量
        """
        if read_env:
            env_varible = os.environ.get("IPECKER_ENV_TYPE", None)
        else:
            env_varible = None
        if env_varible and env_varible.lower() in ENV_TYPES_DICT:
            env = env_varible
        elif env:
            pass
        else:
            env = "online"
        env_desc = ENV_TYPES_DICT.get(env.lower())
        self.last_env = env_desc
        try:
            action1 = TouchAction(self.device.driver)
            el = self.device.find_element_by_id('com.qiyi.gamecenter:id/gc_user_setting_app_version')
            text = el.get_attribute('text')
            for i in range(6):
                if env_desc in text:
                    return True
                else:
                    action1.long_press(el, None, None, 3000).release().perform()
                    time.sleep(2)
                    text = el.get_attribute('text')
        except Exception as e:
            return False
        return False

    def switch_back_environment(self):
        """
        切回上次的环境变量
        """
        if self.last_env:
            self.switch_environment(self.last_env, read_env=False)
        return True

    def setting_back_to_home(self):
        """
        设置页返回至home页
        Returns:
            True: 返回home页成功， False: 返回页失败
        """
        for i in range(2):
            self.back_common_title()
            time.sleep(1)
        try:
            self.device.find_element_by_xpath(self.conf.gamecenter_newgame.xpath, timeout=10)
            return True
        except:
            g_logger.error("从配置页回退到Home页失败")
            return False

    def vertical_game_open(self, game_name):
        """
        纵向游戏更新
        Args:
            game_name: 游戏名
        Returns:
            True: 点击打开成功, False: 点击打开失败
        """
        game_button_xpath = self.conf.vertical_game_list_without_title.xpath_button.format(game_name)
        status = self.get_game_button_status(game_name)
        if status not in (GameButtonStatus.open, GameButtonStatus.click_play):
            g_logger.error("游戏{}按钮不处于打开[点击即玩][打开]状态".format(game_name))
            return False

        try:
            self.device.click_by_xpath(xpath=game_button_xpath, timeout=30)
            time.sleep(5)
            if self.device.get_manufacturer() == 'xiaomi':
                try:
                    self.device.click_by_xpath(self.conf.common_button.xpath_allow, timeout=10)
                    time.sleep(2)
                except:
                    pass

            return True
        except:
            g_logger.error("点击游戏{}按钮失败".format(game_name))
            return False

    def vertical_game_button_install(self, game_name, direction='up'):
        """
        不带标题的纵向游戏下载
        Args:
            game_name: 游戏名
            direction: 滑动方向
        Returns:
            True: 安装成功， False: 安装失败
        """
        if isinstance(game_name, list):
            game_name = game_name[0]
        status = self.get_game_button_status(game_name, direction=direction)
        if status in (GameButtonStatus.install, GameButtonStatus.download):
            game_button_xpath = self.conf.vertical_game_list_without_title.xpath_button.format(game_name)
            for i in range(2):
                try:
                    self.device.click_by_xpath(xpath=game_button_xpath, desc="点击游戏列表下载/安装按钮", timeout=30)
                    time.sleep(5)
                except:
                    g_logger.error("点击游戏按钮状态失败")
                    return False
                if self.game_install(game_name, click_last_installed=False, open_game=False, button_xpath=game_button_xpath):
                    return True
                else:
                    g_logger.info("第一次下载后没有调起安装界面，回退页面，重新下载")
                    self.cmd_back_and_find_ele(xpath=game_button_xpath)
                    continue
            else:
                g_logger.error("点击游戏按钮状态后，下载安装游戏失败")
                return False


        else:
            g_logger.warning("游戏不处于下载状态, 不进行下载".format(GameButtonStatus.get_desc(status)))
            return True

    def get_game_button_status(self, game_name, direction='up'):
        """
        检测游戏按钮状态
        Args:
            game_name: 游戏名
            direction: 查找游戏时滑动方向
        Returns:
            游戏状态
        """
        game_button_xpath = self.conf.vertical_game_list_without_title.xpath_button.format(game_name)
        game_button_ele = self.device.swipe_find_ele_by_xpath(game_button_xpath, direct=direction, rate=0.4, timeout=120)
        if not game_button_ele:
            return False
        if self.device.check_ele_on_bottom(game_button_ele):
            self.device.swipe_screen(rate=0.3)
            game_button_ele = self.device.swipe_down_find_ele(xpath=game_button_xpath, timeout=30)
            if not game_button_ele:
                return False

        x_start, y_start, x_end, y_end = self.device.get_ele_coordinate(game_button_ele)
        icon_path = os.path.join(g_resource['testcase_log_dir'], "game_icon.png")
        screen_path = os.path.join(self.conf_img_dir, "screen.png")
        self.device.get_screenshot_as_file(screen_path)
        if not self.cron_img(screen_path, icon_path, x_start, y_start, x_end, y_end):
            return False
        return self._img_check_game_status(icon_path)

    def _img_check_game_status(self, img_path):
        """
        通过图片对比，检测游戏状态
        Args:
            img_path: 截图保存的游戏按钮图片路径
        Returns:

        """
        height = self.device.get_window_size().get('height')
        if height in(2280, 1792):
            height = 1920
        elif height in (2880, 2712):
            height = 2880
        # import glob
        # button_pic_list = glob.glob(os.path.join(self.conf_img_dir, "{}_*.png".format(height)))
        # if not button_pic_list:
        #     g_logger.warning("未找到分辨率：{}的游戏按钮状态图片".format(height))
        # for butto n_pic in button_pic_list:
        button_pic_list = ['download', 'click_play', 'install', 'open']
        for button_pic in button_pic_list:
            result = self.match_image(img_path, os.path.join(self.conf_img_dir, "{}_{}.png".format(height, button_pic)), confidence=0.85)
            if result:
                # try:
                #     status = os.path.split(button_pic)[1].split("_", 1)[1].split(".")[0]
                #     return status
                # except:
                #     g_logger.error("获取游戏按钮图片路径的按钮状态文字失败")
                return button_pic
        return None

    def small_game_tab_goto_small_game_center(self):
        """
        小游戏没有游戏点击去玩小游戏
        Returns:
            True: 点击去玩小游戏成功，False: 点击失败
        """
        tab_num = self._get_check_tab_num("小游戏")
        if tab_num != 0:
            g_logger.warning("用户已玩过小游戏，没有去玩小游戏提示")
            return False
        try:
            ele = self.device.find_element_by_id(self.conf.tv_empty_prompt.id, timeout=10)
            g_logger.info("小游戏空tab提示: {}".format(ele.get_attribute('text')))
        except:
            g_logger.warning("查找小游戏空tab提示失败")
            return False
        try:
            self.device.click_by_xpath(self.conf.my_info_small_game_tab.xpath_to_small_gc_button, desc="点击去玩小游戏", timeout=10)
            time.sleep(3)
            return True
        except:
            return False

    def click_booked_tab(self):
        """
        点击已预约tab
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.click_tab(self.conf.my_info_tab.booked_name)

    def check_booked_tab_ui(self, game_name=None, timeout=240):
        """
        检测已预约tab UI
        Args:
            游戏
        Returns:
            True: 检测成功, False: 检测失败
        """
        return self.check_tab_ui(self.conf.my_info_tab.booked_name, game_name=game_name, timeout=timeout)

    def check_book_game(self, game_name=None):
        """
        检测已预约游戏，若没有预约，则有空页面提示
        Returns:
            True: 检测成功, False: 检测失败
        """
        tab_num = self._get_check_tab_num(self.conf.my_info_tab.booked_name)
        if tab_num == 0:
            try:
                ele = self.device.find_element_by_id(self.conf.tv_empty_prompt.id, timeout=5)
                g_logger.info("用户未预约任何游戏，页面显示：{}".format(ele.get_attribute('text')))
            except:
                g_logger.error("用户未预约任何游戏，页面不为空")
                return False
        else:
            if game_name:
                return self.check_booked_tab_ui(game_name=game_name)
        return True

    def click_my_gift(self):
        """
        点击我的礼包
        Returns:
            True: 点击成功, False: 点击失败
        """
        return self.device.click_textview_text("礼包", timeout=10)

    """
    我的礼包页
    """
    def check_my_gift_page_ui(self):
        """
        检测我的礼物页面UI
        Returns:
            True: 检测成功, False: 检测失败
        """
        title_xpath = self.conf.comment_title.xpath.format("我的礼包")
        try:
            self.device.find_element_by_xpath(title_xpath, timeout=10)
        except:
            g_logger.error("检测我的礼包标题失败")
            return False
        # 查找我领取的礼包游戏
        eles = self.device.find_elements_by_xpath(self.conf.gift_game_list.xpath_games)
        gift_game_list = [ele.get_attribute("text") for ele in eles]
        if not gift_game_list:
            g_logger.warning("未找到礼包游戏")
            try:
                ele = self.device.find_element_by_xpath(self.conf.tv_empty_prompt.xpath, timeout=10)
                g_logger.warning("页面信息: {}".format(ele.get_attribute('text')))
                return True
            except Exception as e:
                g_logger.error("查找空页面信息失败")
                return False

        for game_name in gift_game_list:
            gift_name_eles = self.device.find_elements_by_xpath(self.conf.gift_game_list.xpath_game_gifts.format(game_name))
            g_logger.info("游戏：{}的礼包为：\n\t{}".format(game_name, ", ".join([ele.get_attribute('text') for ele in gift_name_eles])))

        return True

    def gift_into_gift_detail(self, gift_name):
        """
        游戏礼包页进入礼物详情页
        Returns:
            True: 游戏礼包页点击成功， False: 点击失败
        """
        ele = self.device.swipe_down_find_ele(xpath=self.conf.gift_game_list.xpath_gift.format(gift_name), timeout=30)
        if ele:
            ele.click()
            time.sleep(3)
            return True
        else:
            g_logger.error("点击礼包名,进入礼包详情页失败")
            return False

    def gift_into_game_detail(self, game_name):
        """
        游戏礼包页进入游戏详情页
        Args:
            game_name: 游戏名
        Returns:
            True: 游戏礼包也点击游戏名成功, False: 点击失败
        """
        xpath = self.conf.gift_game_list.xpath_game.format(game_name)
        ele = self.device.swipe_down_find_ele(xpath=self.conf.gift_game_list.xpath_game.format(game_name), timeout=30)
        if ele:
            ele.click()
            time.sleep(3)
            return True
        else:
            g_logger.error("点击游戏名,进入游戏详情页失败")
            return False

    """
    我的礼包详情页
    """
    def check_gift_detail_ui(self, gift_name):
        """
        检测礼包详情页UI
        Args:
        Returns:
            True: 检测成功， False: 检测失败
        """

        try:
            self.device.find_elements_by_xpath(self.conf.comment_title.xpath.format("礼包详情"), timeout=15)
        except:
            g_logger.error("检测礼包详情页标题失败")
            return False
        try:
            self.device.find_elements_by_xpath(self.conf.gift_detail.xpath_gift_name.format(gift_name), timeout=5)
        except:
            g_logger.error("获取礼包名失败")
            return False

        info_title_tupple = ("适用平台", "适用区服", "礼包有效期限", "礼包详情", "兑换说明")
        for info_title in info_title_tupple:
            ele = self.device.swipe_down_find_ele(xpath=self.conf.gift_detail_info_title.xpath_desc.format(info_title), timeout=20)
            if ele:
                g_logger.info("{}:{}".format(info_title, ele.get_attribute('text')))
            else:
                g_logger.info("未找到{}的描述".format(info_title))
                return False

        return True

    """
    设置页
    """
    def click_setting(self):
        """
        点击设置图标，进入设置页
        Returns:
            True: 点击成功, False: 点击失败
        """
        try:
            self.device.click_by_id(self.conf.my_info_setting.id, desc="点击个人中心设置图标", timeout=20)
            time.sleep(3)
            return True
        except:
            return False

    def check_setting_ui(self):
        """
        检测设置页UI
        Returns:
            True: 检测成功, False: 检测失败
        """
        try:
            self.device.find_element_by_xpath(self.conf.comment_title.xpath.format("设置"), timeout=5)
        except Exception as e:
            g_logger.error("检测设置表标题失败")
            return False

        expect_set = {"消费记录", "反馈", "游玩时间控制"}
        eles = self.device.find_elements_by_xpath("//android.widget.TextView", timeout=5)
        text_set = {ele.get_attribute("text") for ele in eles}
        g_logger.info("检测到的textview集合：\n\t{}".format("\n\t".join(text_set)))
        return expect_set.issubset(text_set)

    def setting_into_submit(self):
        """
        设置页进入提交反馈页
        Returns:
            True: 点击提交反馈入口成功, False: 点击失败
        """
        return self.device.click_textview_text("反馈")

    def submit_feedback(self, feedback_info, feedback_type="其他", contact=None):
        """
        设置页提交反馈
        Returns:
            feedback_info: 反馈的信息
            feedback_type: 反馈类型，包含: 游戏下载失败, 福利/礼包少, 找不到想要的游戏, 其他
            contact: 联系方式
        """
        try:
            g_logger.info("选择反馈类型: {}".format(feedback_type))
            self.device.click_by_xpath(self.conf.feedback.xpath_type.format(feedback_type), timeout=15)
            time.sleep(1)
        except:
            g_logger.error("反馈类型：{} 没有找到".format(feedback_type))
            return False

        try:
            g_logger.info("填写反馈信息: {}".format(feedback_info))
            self.device.find_element_by_id(self.conf.feedback.id_content, timeout=10).set_text(feedback_info)
        except:
            g_logger.error("反馈内容框没有找到")
            return False

        if contact:
            try:
                g_logger.info("填写联系方式: {}".format(contact))
                self.device.find_element_by_id(self.conf.feedback.id_contact, timeout=10).set_text(contact)
            except:
                g_logger.error("反馈内容框没有找到")
                return False
        self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "submit.png"))
        try:
            g_logger.info("提交反馈")
            self.device.click_by_id(self.conf.feedback.id_submit, timeout=5)
            time.sleep(2)
        except:
            g_logger.error("提交按钮没有找到")
            return False

        return True

    def setting_into_game_time_limit(self):
        """
        设置页进入游戏时间控制
        Returns:
            True: 点击游玩时间控制成功，False: 点击失败
        """
        return self.device.click_textview_text("游玩时间控制")

    def open_game_time_limit(self):
        """
        打开游玩时间控制
        Returns:
            True: 打开成功, False: 打开失败
        """
        if not self.device.check_textview_text("游玩时间控制", timeout=15):
            g_logger.error("检测游玩时间标题失败")
            return False

        try:
            self.device.find_element_by_id(self.conf.game_time_limit.id_minus, timeout=5)
            g_logger.info("游玩时间控制已处于打开状态")
            return True
        except:
            pass

        try:
            self.device.click_by_xpath(self.conf.game_time_limit.xpath_switch_button, desc="点击打开游玩时间控制开关", timeout=5)
            time.sleep(2)
        except:
            return False

        try:
            self.device.find_element_by_id(self.conf.game_time_limit.id_minus, timeout=5)
            return True
        except:
            g_logger.info("检测游玩时间控制时长设置按钮失败")
            return False

    def close_game_time_limit(self):
        """
        关闭游玩时间控制
        Returns:
            True: 关闭成功, False: 关闭失败
        """
        if not self.device.check_textview_text("游玩时间控制", timeout=15):
            g_logger.error("检测游玩时间标题失败")
            return False

        try:
            self.device.find_element_by_id(self.conf.game_time_limit.id_minus, timeout=5)
        except:
            g_logger.info("游玩时间控制已处于关闭状态")
            return True

        try:
            self.device.click_by_xpath(self.conf.game_time_limit.xpath_switch_button, desc="点击打开游玩时间控制开关", timeout=5)
            time.sleep(2)
        except:
            return False

        try:
            self.device.find_element_by_id(self.conf.game_time_limit.id_minus, timeout=5)
            g_logger.info("检测到游玩时间控制时长设置按钮, 按钮未关闭")
            return False
        except:
            return True

    def setting_check_game_time_limit_open(self):
        """
        设置页检测游玩时间按钮是否打开
        Returns:
            True: 处于打开状态, False: 处于关闭状态
        """
        try:
            ele = self.device.find_element_by_id(self.conf.my_info_setting.id_game_time_limit_status, timeout=10)
            return ele.get_attribute('text') == "开启"
        except:
            g_logger.error("设置页查找游玩时间控制开关状态元素失败")
            return None

    def setting_check_shortcut(self):
        """
        设置页检测'测添加爱奇艺游戏中心至桌面'文本是否存在
        Returns:
            True: 检测成功, False: 检测失败
        """
        return self.device.check_textview_text("添加爱奇艺游戏中心至桌面", timeout=15)

    def setting_click_shortcut(self):
        """
        设置页点击'测添加爱奇艺游戏中心至桌面'文本是否存在
        Returns:
            True: 检测成功, False: 检测失败
        """
        return self.device.click_textview_text(self.conf.setting_entrance.shortcut, timeout=15)

    def _check_shortcut_prompt_ui(self):
        """
        检测设置页点击'添加爱奇艺游戏中心至桌面'后弹出的温情提示页面
        Returns:
            True: 检测成功, False: 检测失败
        """
        setting_shortcut_name = self.conf.setting_entrance.shortcut
        if not self.device.check_textview_text("温馨提示", timeout=5):
            g_logger.info("未找到温馨提示弹窗，查看是否在设置页")
            if not self.device.click_textview_text(setting_shortcut_name, timeout=5):
                return False
        g_logger.info("检测查看原因按钮功能")
        try:
            self.device.click_by_xpath("//android.widget.Button[@text='查看原因']", desc='点击查看原因', timeout=10)
            time.sleep(2)
            self.device.find_element_by_xpath(self.conf.comment_title.xpath.format("查看原因"), timeout=10)
            eles = self.device.find_elements_by_xpath("//android.widget.TextView")
            g_logger.info("页面信息为：")
            for ele in eles:
                g_logger.info("\t{}".format(ele.get_attribute('text')))
            g_logger.info("回退到设置页")
            self.back_common_title()  #
            self.device.click_textview_text(setting_shortcut_name, timeout=5)
        except:
            g_logger.error("检测查明原因按钮功能失败")
            return False

        g_logger.info("查看不用了按钮功能")
        try:
            self.device.click_by_xpath("//android.widget.Button[@text='不用了']", desc='点击不用了', timeout=10)
            time.sleep(2)
        except:
            g_logger.error("检测不用了按钮功能失败")
            return False

        return True

    def check_setting_shortcut(self):
        """
        检测设置页添加快捷方式功能， 需要进入到设置页
        Returns:
            True: 检测成功, False: 检测失败
        """
        g_logger.info("检测桌面是否已经创建了快捷方式")
        check_desktop_ret = self.check_desktop_app(self.conf.gc_app_shortcut.name)
        if not check_desktop_ret:
            if self.device.get_manufacturer() == 'oppo':
                self._oppo_phone_manager_gant("创建桌面快捷方式", app_name="爱奇艺", page_type='switch')
                time.sleep(1)
            else:
                self.device.adb.grant_shortcut("com.qiyi.video")  # 授权基线添加桌面快捷方式

        self.into_desktop_app(self.conf.base_app.name, need_back_home=True, timeout=60)
        time.sleep(2)
        if not check_desktop_ret:
            g_logger.info("游戏中心桌面快捷方式未找到，添加快捷方式")
            if not self.setting_check_shortcut():
                g_logger.info("设置页'添加爱奇艺游戏中心至桌面'未找到，检测失败")
                return False
            self.setting_click_shortcut()


            try:
                # self.device.find_element_by_xpath(self.conf.gamecenter_add_to_desktop_title.xpath, timeout=2)
                self.device.find_element_by_xpath(self.conf.gamecenter_add_to_desktop_button.xpath, timeout=10).click()  # 点击添加
                time.sleep(2)
            except:
                pass
            if self.device.get_manufacturer() == 'oppo':
                g_logger.info("oppo手机，通过快捷方式检测是否生成了快捷方式")
                return self.check_desktop_app(self.conf.gc_app_shortcut.name)
        else:
            g_logger.info("游戏中心桌面快捷方式已找到")
            if not self.setting_check_shortcut():
                g_logger.info("设置页'添加爱奇艺游戏中心至桌面'未找到，检测成功")
                return True
            self.setting_click_shortcut()

        return self._check_shortcut_prompt_ui()










