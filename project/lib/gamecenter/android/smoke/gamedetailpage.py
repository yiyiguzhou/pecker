# -*- coding: UTF-8 -*-

"""
File Name:      gamedetailpage
Author:         zhangwei04
Create Date:    2018/11/19
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from framework.utils.threads import IpeckerThread
from project.lib.gamecenter.android.smoke.common import Common


class GameDetailPage(Common):
    """游戏详情页"""

    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)

        self.is_clicked_bubble_circle_full_screen = False

    def check_ui(self, game_name=None, version="当前版本：", pgk_size="游戏大小：", publish_date="更新日期：", developer="开 发 商：", sys_require="系统要求：",
                 click_tab=False, timeout=90):
        """
        检查页面UI
        Args:
            game_name: 游戏名称
            version: 版本
            pgk_size: 游戏大小
            publish_date: 游戏发行\更新日期
            developer: 游戏开发商
            sys_require: 系统要求
            click_tab: 是否点击详情Tab
            timeout: 查找超时
        Returns:
            True: 页面检查成功 False: 页面检查失败
        """
        if click_tab:
            self._click_tab("详情", check_tab_selected=False)
        else:
            time.sleep(2)

        if game_name:
            try:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_name), timeout=10)
            except:
                g_logger.error("游戏详情页查找游戏名失败")
                return False

        time.sleep(1)
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')

        # 滑动查找游戏详细信息
        time_start = time.time()
        find_text_set = [ele for ele in (version, pgk_size, publish_date, developer, sys_require) if ele not in (None, "", " ")]
        if not find_text_set:
            g_logger.info("不检查版本等信息")
            return True

        while timeout > time.time() - time_start:
            try:
                remove_text_list = []
                for text in find_text_set:
                    self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(text), timeout=5)
                    remove_text_list.append(text)
            except Exception as e:
                self.device.swipe(width / 2, height * 6 / 10, width / 2, height * 3 / 10)
                time.sleep(2)
                continue
            finally:
                for text in remove_text_list:
                    find_text_set.remove(text)
                if not find_text_set:
                    return True
        g_logger.warning("未找到以下信息：{}".format(",".join(find_text_set)))
        return False

    def game_downlaod_pause_install(self, game_name, open_game=True):
        """
        游戏下载、暂停、继续下载至安装完成接口
        Args:
            game_name: 游戏名
            open_game: 是否打开游戏
        Returns:
            True: 游戏下载至安装完成流程执行ok，False: 流程步骤出现失败
        """
        dl_xpath = "//android.widget.LinearLayout[@resource-id='com.qiyi.gamecenter:id/details_bottom_layout']//android.widget.ProgressBar"
        try:

            self.device.click_by_xpath(dl_xpath, desc='点击下载', timeout=10)
            self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "downloading.png"))
        except:
            g_logger.error("查找：查找下载按钮失败")
            return False
        # 暂停1秒
        try:
            time.sleep(1)
            self.device.click_by_xpath(dl_xpath, desc='点击暂停', timeout=10)
            self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "pause.png"))
        except:
            g_logger.error("暂停：查找下载按钮失败")
            return False
        # 继续
        try:
            self.device.click_by_xpath(dl_xpath, desc='继续下载', timeout=10)
        except:
            g_logger.error("继续：查找下载按钮失败")
            return False

        return self.game_install(game_name, open_game=open_game, timeout=600, button_xpath=dl_xpath)

    def check_video_start_img(self, game_name, img_name, video_time=300):
        """
        检测视频不放片图
        Args:
            game_name: 游戏名
            img_name: 期望片图名字前缀，配置在project/conf/img目录下，如"doudizhu"
            video_time: 视频时长
        Returns:
        """
        width = self.device.get_window_width()
        if width == 720:
            img_name = "video_start_720_{}.png".format(img_name)
        elif width == 1440:
            img_name = "video_start_1440_{}.png".format(img_name)
        else:
            img_name = "video_start_{}.png".format(img_name)

        # if not self.device.check_textview_text(game_name, timeout=10):
        #     g_logger.error("检测游戏详情页游戏名失败")
        #     return False
        # time.sleep(2)
        # TODO: 若游戏详情页视频不自动不放需要修改此处逻辑
        screen_file_path = os.path.join(g_resource['testcase_log_dir'], "screen_shot.png")
        pic_video_start = os.path.join(self.conf_img_dir, img_name)
        video_id = self.conf.video_play.id
        for i in range(2):
            try:
                seconds = self.get_video_play_time(video_id=video_id)
                if not seconds:
                    g_logger.info("未找到视频时长，采用默认超时方式300s")
                    time_start = time.time()
                    while video_time > time.time() - time_start:
                        try:
                            self.device.find_element_by_id(self.conf.detail_video_play.id, timeout=5)
                            break
                        except:
                            time.sleep(1)
                else:
                    g_logger.info("sleep{}秒, 等待视频播放结束".format(seconds))
                    time.sleep(seconds)
                    self.device.find_element_by_id(self.conf.detail_video_play.id, timeout=5)
                self.device.get_screenshot_as_file(screen_file_path)  # 截图
                result = self.match_image(screen_file_path, pic_video_start)
                if result:
                    print(result)
                    return True
                else:
                    g_logger.error("图像对比失败")
                    return False
            except:
                pass

        return False

    def click_play_without_download(self):
        """点击免下载畅玩按钮
        Returns:
            True: 点击成功， False: 未找到按钮
        """
        try:
            self.device.click_by_id(self.conf.gd_play_without_download.id, desc="查找免下载畅玩按钮", timeout=20)
            time.sleep(5)
            return True
        except:
            return False

    def check_detail_ui(self, game_name, titles, version="", pgk_size="", publish_date="更新日期：", developer="开 发 商：", sys_require="", timeout=240):
        """
        通过一些标题检测详情页UI
        Returns:
            True: 检测成功， False: 检测失败
        """

        if not self.check_ui(game_name, version=version, pgk_size=pgk_size, publish_date=publish_date, developer=developer, sys_require=sys_require,
                             timeout=60):
            g_logger.error("检查游戏详情页UI失败")
            return False
        if titles:
            if isinstance(titles, str):
                titles = [titles]
            ele_xpaths = [self.conf.template_title_tv.xpath.format(title) for title in titles]
            order_texts = self.device.swipe_down_find_text_by_xpath(ele_xpaths, rate=0.3, timeout=timeout)
            g_logger.info("期望值列表：{}".format(titles))
            return order_texts == titles
        else:
            return True

    def detail_goto_all_welfare(self):
        """
        查找全部福利
        Returns:
            True: 查找成功， False: 查找失败
        """
        xpath = '//android.widget.TextView[contains(@text, "个福利") and @resource-id="com.qiyi.gamecenter:id/template_bottom_find_all_text"]'
        ele = self.device.swipe_down_find_ele(xpath=xpath, timeout=120)
        if ele:
            try:
                bottom_ele = self.device.find_element_by_id(self.conf.gd_bottom_layout.id, timeout=10)
                if self.device.check_ele_on_ele(ele, bottom_ele):
                    self.device.swipe_screen(rate=0.3)
                    time.sleep(2)
                    ele = self.device.find_element_by_xpath(xpath, timeout=10)
            except:
                pass
            ele.click()
            time.sleep(3)
            return True
        else:
            g_logger.error("查找全部福利失败")
            return False

    def check_welfare_ui(self, titles=None):
        """
        检查福利Tab UI
        Args:
            titles: 检测标题列表
        Returns:

        """
        if not self._check_tab_is_selected("福利"):
            return False

        if titles:
            if isinstance(titles, str):
                titles = [titles]
            ele_xpaths = [self.conf.template_title_tv.xpath.format(title) for title in titles]
            order_texts = self.device.swipe_down_find_text_by_xpath(ele_xpaths, rate=0.3, timeout=240)
            return order_texts == titles
        else:
            return True

    def check_bubble_circle_tab(self):
        """
        检测游戏圈tab
        Returns:
            True: 检测成功， False: 检测失败
        """
        return self._check_tab_is_selected("游戏圈")

    def detail_get_bubble_circle_counts(self):
        """获取详情tab游戏圈用户名
        Returns:
            list： 用户名列表
        """
        count_list = self.device.get_texts_between_xpath(find_xpath=self.conf.bubble_circle_rv.xpath_user_name, start_xpath=self.conf.bubble_circle_rv.xpath_title,
                                      end_xpath=self.conf.bubble_circle_rv.xpath_more, timeout=240)
        if count_list:
            g_logger.info("详情tab游戏圈用户：{}".format(",".join(count_list)))
        else:
            g_logger.info("获取详情tab游戏圈用户失败")
        return count_list

    def detail_goto_more_bubble_circle(self):
        """
        详情tab进入游戏圈tab
        Returns:
            True: 进入成功， False: 进入失败
        """
        # count_list = self.detail_get_bubble_circle_counts()
        # if not count_list:
        #     return False
        # if count_list < 3:
        #     try:
        #         self.device.click_by_xpath(self.conf.bubble_circle_rv.xpath_more, timeout=5)
        #         g_logger.error("用户数小于3, 显示更多游戏圈")
        #         return False
        #     except:
        #         g_logger.info("用户数小于3, 未显示更多游戏圈")
        #         return True
        #
        # try:
        #     self.device.click_by_xpath(self.conf.bubble_circle_rv.xpath_more, timeout=10)
        #     time.sleep(2)
        #     return True
        # except:
        #     g_logger.error("查找更多游戏圈失败")
        #     return False

        ele = self.device.swipe_down_find_ele(self.conf.bubble_circle_rv.xpath_more, timeout=240)
        if ele:
            bottom_ele = self.device.find_element_by_id(self.conf.gd_bottom_layout.id, timeout=10)
            if self.device.check_ele_on_ele(ele, bottom_ele):
                self.device.swipe_screen(rate=0.3, direction='up')
            ele = self.device.swipe_down_find_ele(self.conf.bubble_circle_rv.xpath_more, timeout=10)
            ele.click()
            time.sleep(5)
            return True
        else:
            g_logger.error("查找更多游戏圈失败")
            return False

    def _check_tab_is_selected(self, tab_name):
        """
        检测tab被勾选
        Args:
            tab_name: tab名
        Returns:
            True: 检测成功，已勾选，False: 检测失败
        """
        tab_xpath = self.conf.gd_tab.xpath.format(tab_name)
        try:
            self.device.find_element_by_xpath(tab_xpath, timeout=10)
            time.sleep(3)   # 等待元素出现稳定再重新捕获
            ele = self.device.find_element_by_xpath(tab_xpath, timeout=10)
            selected = ele.get_attribute('selected')
            time.sleep(0.5)
            if not selected == "true":
                g_logger.error("{}tab未被选中".format(tab_name))
                return False
        except:
            g_logger.error("未找到{}tab".format(tab_name))
            return False
        return True

    def _get_more_play_game_name(self):
        """
        获取大家还在玩游戏列表
        Returns:
            list: 游戏列表  False: 获取失败
        """
        start_xpath = "//android.widget.TextView[@text='大家还在玩']"
        game_list = self.device.get_texts_between_xpath(find_xpath=self.conf.gd_more_play.xpath_game_name, start_xpath=start_xpath,
                                                  end_xpath=self.conf.gd_more_play.xpath_bottom, rate=0.5, timeout=240)
        return game_list

    def check_more_play_game(self, max_num=8):
        """
        检测详情Tab大家还在玩游戏推荐
        Returns:

        """
        game_list = self._get_more_play_game_name()
        if not game_list:
            g_logger.error("获取游戏信息失败")
            return False

        return len(game_list) < max_num + 1

    def welfare_into_gift_detail(self, gift_name=None):
        """
        福利进入礼包详情
        Args:
            gift_name: 礼物名称，若未传入此参数则点击第一个礼包
        Returns:
            True: 找到礼包并点击， False: 未找到礼包
        """
        if gift_name:
            xpath = self.conf.gd_welfare_gift.xpath_gift_name.format(gift_name)
        else:
            xpath = self.conf.gd_welfare_gift.xpath_first_detail
        ele = self.device.swipe_down_find_ele(xpath=xpath, timeout=120)
        if ele:
            bottom_ele = self.device.find_element_by_id(self.conf.gd_bottom_layout.id, timeout=5)
            if self.device.check_ele_on_ele(ele, bottom_ele):
                self.device.swipe_screen(rate=0.3, direction="up")
                try:
                    self.device.click_by_xpath(xpath=xpath, timeout=5)
                except:
                    g_logger.warning("检测礼包详情页和底部重叠，向上滑动后，没有找到礼包详情页")
                    return False
            else:
                ele.click()

            time.sleep(2)

        else:
            g_logger.error("搜索福利-有码礼包失败")
            return False

        return True

    def check_gift_detail_ui(self):
        """
        检测礼物详情页UI
        Returns:
            True: 检测成功，False: 检测失败
        """
        try:
            self.device.find_element_by_xpath(self.conf.gd_gift_detail.xpath_title, timeout=10)
            return True
        except:
            return False

    def into_welfare_tab(self):
        """
        进入福利页Tab
        Returns:
            True: 进入成功， False: 进入失败
        """
        return self._click_tab("福利")

    def into_bubble_circle_tab(self):
        """
        进入游戏圈Tab
        Returns:
            True: 进入成功， False: 进入失败
        """
        return self._click_tab("游戏圈", check_tab_selected=False)

    def _click_tab(self, tab_name, check_tab_selected=True):
        """
        进入福利页Tab
        Args:
            tab_name: 标签名
            check_tab_selected: 是否检测tab选中
        Returns:
            True: 进入成功， False: 进入失败
        """
        time.sleep(5)  # 等待5秒，待页面稳定
        xpath = self.conf.gd_tab.xpath.format(tab_name)
        try:
            self.device.click_by_xpath(xpath, desc="点击Tab:{}".format(tab_name), timeout=10)
            time.sleep(5)
            if check_tab_selected:
                return self._check_tab_is_selected(tab_name)
            else:
                return True
        except Exception as e:
            g_logger.warning(str(e))
            return False

    def welfare_goto_fisrt_activity(self):
        """
        福利Tab进入第一个专属活动
        Returns:
            True: 进入成功, False: 进入失败
        """
        if not self.device.check_textview_text('专享活动', swipe=True, timeout=120):
            g_logger.error("福利Tab查找专享活动失败")
            return False
        # 点击专享活动第一个活动
        ele = self.device.swipe_down_find_ele(xpath=self.conf.gd_welfare_activity.xpath_first_activity)
        try:
            bottom_ele = self.device.find_element_by_id(self.conf.gd_bottom_layout.id, timeout=5)
            if self.device.check_ele_on_ele(ele, bottom_ele):
                self.device.swipe_screen(direction="up")
        except:
            pass
        try:
            self.device.click_by_xpath(self.conf.gd_welfare_activity.xpath_first_activity, timeout=10)
            time.sleep(2)
            return True
        except:
            g_logger.error("点击第一个图片失败")
            return False

    def check_bubble_circle_ui(self):
        """
        检测游戏圈UI布局
        Returns:
            True: 检测成功， False: 检测失败
        """
        # self.conf.gd_bubble_circle.id_refresh
        # 检测公告
        try:
            ele = self.device.find_element_by_xpath(self.conf.gd_bubble_circle.xpath_title, timeout=10)
            g_logger.info("公告信息：{}".format(ele.get_attribute("text")))
        except:
            g_logger.warning("没有找到公告信息")

        # 检测发布按钮
        try:
            self.device.find_element_by_id(self.conf.gd_bubble_circle.id_send, timeout=10)
            g_logger.error("找到发布按钮")
        except:
            g_logger.error("没有找到发布按钮")
            return False

        # 检测用户信息
        try:
            ele = self.device.find_element_by_xpath(self.conf.gd_bubble_circle.xpath_user_name, timeout=5)
            g_logger.info("用户名：{}".format(ele.get_attribute("text")))
            ele = self.device.find_element_by_xpath(self.conf.gd_bubble_circle.xpath_send_time, timeout=5)
            g_logger.info("发布时间：{}".format(ele.get_attribute("text")))
        except:
            g_logger.warning("没有找到用户发布的评论信息")
            return False

        return True

    def bubble_circle_detail_back(self):
        """
        游戏圈棋牌中心详情页，返回按钮
        Returns:
            True: 返回成功， False: 返回失败
        """
        try:
            self.device.click_by_id("com.qiyi.video:id/title_bar_left", desc="点击返回按钮，返回至基线", timeout=10)
            return True
        except:
            g_logger.warning("泡泡详情页返回游戏详情页失败")
            return False

    def bubble_circle_into_notice(self, need_back=True):
        """
        游戏圈进入公告
        Args:
            need_back: 是否需要返回
        Returns:
            True: 进入成功， False: 进入失败
        """
        try:
            ele = self.device.find_element_by_xpath(self.conf.gd_bubble_circle.xpath_title, timeout=10)
            notice = ele.get_attribute("text")
            g_logger.info("公告内容：{}".format(notice))
            ele.click()
            time.sleep(3)
        except:
            g_logger.error("未找到公告")
            return True
        # 检查是否进入泡泡详情页
        try:
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺棋牌中心']", timeout=20)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺棋牌君']", timeout=10)
        except:
            g_logger.error("检测公告详情页失败")
            return False
        if need_back:
            return self.bubble_circle_detail_back()
        else:
            return True

    def bubble_circle_into_message(self, need_back=True):
        """
        游戏圈进入泡泡消息详情
        Args:
            need_back: 是否需要返回
        Returns:
            True: 进入成功， False: 进入失败
        """
        time.sleep(5)   # 等待更新弹出消失
        ele = self.device.swipe_down_find_ele(xpath=self.conf.gd_bubble_circle.xpath_msg_desc, timeout=60)
        if ele:
            bottom_ele = self.device.find_element_by_id(self.conf.gd_bottom_layout.id, timeout=5)
            if self.device.check_ele_on_ele(bottom_ele, ele):
                g_logger.info("元素重叠，向下滑动元素")
                self.device.swipe_screen(0.3)
                time.sleep(2)
            ele = self.device.swipe_down_find_ele(xpath=self.conf.gd_bubble_circle.xpath_msg_desc, timeout=60)
            if ele:
                desc = ele.get_attribute("text")
                g_logger.info("发布消息：{}".format(desc))
                ele.click()
                time.sleep(3)
            else:
                g_logger.error("滑动元素后，查找游戏圈用户发布的信息失败")
                return False
        else:
            g_logger.error("点击游戏圈用户发布的信息失败")
            return False

        try:
            self.device.click_by_id(self.conf.bubble_detail_full_screen.id_close, desc='点掉游戏圈详情页弹窗', timeout=5)
            time.sleep(3)
        except:
            pass
        # self.is_clicked_bubble_circle_full_screen = True
        # 检查是否进入泡泡详情页
        try:
            # self.device.find_element_by_xpath("//android.widget.TextView[@text='爱奇艺棋牌中心']", timeout=20)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(desc), timeout=10)
        except:
            try:
                self.device.find_element_by_xpath("//android.view.View[@content-desc='{}']".format(desc), timeout=5)
            except:
                g_logger.error("检测泡泡详发布消息描述失败")
                return False
        if need_back:
            return self.bubble_circle_detail_back()
        else:
            return True

    def bubble_circle_video_follow(self, commment):
        """
        泡泡圈视频转发
        Returns:
            True: 转发成功， False: 转发失败
        """
        # ele_xpath = "//android.widget.TextView[@resource-id='com.qiyi.gamecenter:id/tv_base_line_share_video_duration']"
        ele_xpath = "//android.widget.ImageView[@resource-id='com.qiyi.gamecenter:id/video_play_iv']/../../../../../../../../android.widget.TextView[@resource-id='com.qiyi.gamecenter:id/tv_feed_description']"
        ele = self.device.swipe_down_find_ele(xpath=ele_xpath, rate=0.4, timeout=240)
        if ele:
            # try:
            #     bottom_ele = self.device.find_element_by_id(self.conf.gd_bottom_layout.id, timeout=5)
            #     if self.device.check_ele_on_ele(ele, bottom_ele):
            #         self.device.swipe_screen(rate=0.3, direction='up')
            #         ele = self.device.find_element_by_id(ele_xpath, timeout=10)
            # except:
            #     pass
            # duration_str = ele.get_attribute('text')
            # seconds = self._get_video_duration_seconds(duration_str=ele.get_attribute('text'))
            ele.click()  # 进入泡泡详情页
            time.sleep(3)
        else:
            return False

        # 查找点击分享
        share_buble_xpath = "//android.widget.TextView[@text='分享到']/../..//android.widget.TextView[@text='泡泡']"
        try:
            self.device.swipe_screen(0.2)
            self.device.click_by_xpath(share_buble_xpath, timeout=10)
            time.sleep(3)
        except:
            try:
                self.device.click_by_id("com.qiyi.video:id/title_bar_share", timeout=5)
                time.sleep(2)
                share_buble_xpath = "//android.widget.TextView[@text='分享至']/../..//android.widget.TextView[@text='泡泡']"
                self.device.click_by_xpath(share_buble_xpath, timeout=5)
            except:
                g_logger.warning("查找分享-泡泡失败")
                return False
        # 选择泡泡圈：爱奇艺游戏圈
        if not self._bubble_forward_select_qiyi_game_circle():
            return False
        # 添加发布信息并发布
        comment_xpath = "//android.widget.EditText[@text='说说你的想法吧']"
        try:
            self.device.find_element_by_xpath(comment_xpath, timeout=10).set_text(commment)
            share_button_xpath = "//android.widget.TextView[@text='发布' and (@resource-id)!='com.qiyi.video:id/title_bar_title']"
            self.device.click_by_xpath(share_button_xpath, timeout=5)
            time.sleep(10)
        except:
            g_logger.warning("发布页：查找发布按钮失败")

        # iqiyi_game_circle_title = "//android.widget.TextView[@text='爱奇艺游戏' and @resource-id='com.qiyi.video:id/title_bar_title']"
        iqiyi_game_circle_title = "//android.widget.TextView[@text='爱奇艺游戏']"
        submit_comment_xpath = "//android.widget.TextView[@text='{}']".format(commment)
        try:
            self.device.find_element_by_xpath(iqiyi_game_circle_title, timeout=20)
            try:
                # 转发视频会会有两种页面，先确认是否进入用户发布信息页面，再确认是否是否进入游戏圈首页
                self.device.find_element_by_xpath(submit_comment_xpath, timeout=10)
            except:
                self.device.find_element_by_xpath("//android.widget.TextView[@text='精华']", timeout=10)

            self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "video_forward_submit_success.png"))
            return True
        except:
            g_logger.error("发布后确认已发布页面检测失败")
            return False

    def _bubble_forward_select_qiyi_game_circle(self):
        """
        游戏圈转发选择爱奇艺游戏圈
        Returns:
            True: 选择成功， False: 选择失败
        """
        height = self.device.get_window_height()
        if height in (1280, ):
            bubble_title = os.path.join(self.conf_img_dir, "share_bubble_title_1280.png")
            iqiyi_game_circle = os.path.join(self.conf_img_dir, "share_bubble_iqiyi_game_circle_1280.png")
        else:
            bubble_title = os.path.join(self.conf_img_dir, "share_bubble_title.png")
            iqiyi_game_circle = os.path.join(self.conf_img_dir, "share_bubble_iqiyi_game_circle.png")
        screen_img_path = os.path.join(self.conf_img_dir, "screen.png")
        for i in range(10):
            self.device.get_screenshot_as_file(screen_img_path)
            result = self.match_image(screen_img_path, bubble_title)
            if result:  # 匹配爱奇艺游戏圈
                break
            time.sleep(1)
        else:
            g_logger.warning("图像匹配爱奇艺游戏圈失败")
            return False

        for j in range(5):
            result = self.match_image(screen_img_path, iqiyi_game_circle)
            if result:
                self.device.tap([result['result']])
                time.sleep(3)
                break
            time.sleep(1)
            self.device.get_screenshot_as_file(screen_img_path)
        else:
            g_logger.warning("查找圈子:爱奇艺游戏失败")
            return False

        return True

    def _bubble_circle_local_video_upload(self):
        """
        泡泡圈视频上传(本地视频)
        Returns:
            True: 上传成功， False: 上传失败
        """
        video_xpath = "//android.widget.TextView[@text='视频']"

        try:
            self.device.click_by_xpath(video_xpath, desc='点击发布按钮', timeout=10)
            time.sleep(3)
        except:
            return False

        for i in range(2):
            try:
                local_upload_id = "com.qiyi.video:id/layout_local_video"
                self.device.click_by_id(local_upload_id, desc="视频上传页-点击本地上传按钮", timeout=5)
                time.sleep(3)
                break
            except Exception as e:
                manu = self.device.get_manufacturer()
                if manu == 'xiaomi':
                    loop_num = 2
                else:
                    loop_num = 1
                for j in range(loop_num):
                    if manu in ('vivo', 'oppo', 'xiaomi'):
                        text = '允许'
                    else:
                        text = '始终允许'
                    try:
                        self.device.click_by_xpath("//android.widget.Button[@text='{}']".format(text), desc="点击{}弹框".format(text), timeout=5)
                        time.sleep(2)
                        continue
                    except:
                        break
        try:
            video_view_xpath = "//android.widget.ImageView"
            self.device.click_by_xpath(video_view_xpath, desc="选择第一个本地视频", timeout=20)
            time.sleep(3)
        except:
            return False

        try:
            # video_preview_id = "com.qiyi.video:id/drh"
            # self.device.click_by_id(video_preview_id, desc="点击上传按钮", timeout=20)
            # time.sleep(3)
            video_preview_xpath = "//android.widget.RelativeLayout[@resource-id='com.qiyi.video:id/layout_next']/android.widget.ImageView"
            self.device.click_by_xpath(video_preview_xpath, desc="点击上传按钮", timeout=20)
            time.sleep(3)
        except:
            return False

        return True

    def bubble_circle_share(self, title, content, type=None):
        """
        泡泡圈发布信息
        Args:
            title: 发布标题
            content: 发布内容描述
            type: 发布类型，None: 只有文字， picture: 附带图片, video: 附带视频, vote: 投票
        Returns:
            True: 发布成功, False: 发布失败
        """
        from framework.utils.func import random_str
        content = "{}{}".format(content, random_str())

        try:
            self.device.click_by_id(self.conf.gd_bubble_circle.id_send, timeout=20)
            time.sleep(3)
        except:
            g_logger.error("点击编写分析按钮失败")
            return False

        try:
            self.device.find_element_by_xpath(self.conf.gd_bubble_circle_share.xpath_title, timeout=20).set_text(title)
        except:
            g_logger.error("写入标题失败")
            return False

        try:
            ele = self.device.find_element_by_xpath(self.conf.gd_bubble_circle_share.xpath_content, timeout=20)
            ele.set_text(content)
        except:
            g_logger.error("写入内容失败")
            return False

        # 附件添加
        if type == 'video':
            if not self._bubble_circle_local_video_upload():
                return False

        # 点击发布
        try:
            self.device.click_by_xpath(self.conf.gd_bubble_circle_share.xpath_share_button, timeout=120)
            time.sleep(2)
        except:
            g_logger.error("点击发布失败")
            return False

        self._bubble_circle_click_refresh()
        # 检测是否回到游戏圈
        try:
            self.device.find_element_by_id(self.conf.gd_bubble_circle.id_send, timeout=120)
        except:
            g_logger.error("检查回到游戏圈失败")
            return False

        return True

    def _bubble_circle_click_refresh(self):
        """
        点击弹出的刷新
        Returns:
            True: 点击成功， False: 点击失败
        """
        try:
            self.device.click_by_id(self.conf.gd_bubble_circle.id_refresh, timeout=10)
            time.sleep(2)
            return True
        except:
            g_logger.error("未找到更新弹窗")
            return False

    def check_bubble_circle_refresh(self):
        """
        检测游戏圈刷新功能，暂时不和游戏圈详情推荐排序方式数据对比
        Returns:
            True: 检测成功, False: 检测失败
        """
        g_logger.info("进入消息后再退出：")
        if not self.bubble_circle_into_message(need_back=True):
            return False

        time.sleep(1.5)
        screen_immediate_back = os.path.join(g_resource['testcase_log_dir'], "bubble_detail_back_circle_imd.png")
        self.device.get_screenshot_as_file(screen_immediate_back)
        time.sleep(5)
        screen_back_sleep = os.path.join(g_resource['testcase_log_dir'], "bubble_detail_back_circle_sleep.png")
        des_img = os.path.join(self.conf_img_dir, "bubble_circle_update_comment.png")
        self.device.get_screenshot_as_file(screen_back_sleep)

        ret = True
        result = self.match_image(screen_immediate_back, des_img, confidence=0.8)
        if not result:
            g_logger.error("立即返回未找到更新内容按钮，匹配失败")
            ret = False
        result = self.match_image(screen_back_sleep, des_img, confidence=0.8)
        if result:
            g_logger.error("等待5秒后找到更新内容按钮，匹配失败")
            ret = False
        return ret

        # 通过图像匹配更新按钮情况
        # g_logger.info("检测并点击游戏圈刷新按钮")
        # self._bubble_circle_click_refresh()
        # try:
        #     ele = self.device.find_element_by_xpath(self.conf.gd_bubble_circle.xpath_msg_desc, timeout=10)
        #     desc = ele.get_attribute("text")
        #     g_logger.info("刷新后消息：{}".format(desc))
        # except:
        #     return False
        # return True

    def swipe_check_send_icon(self):
        """
        滑动检测发布图标，向上滑动时，图标不显示；想下滑动时图标显示
        Returns:
            True: 检测成功， False: 检测失败
        """
        ret = True
        height = self.device.get_window_size().get("height", 1024)
        if height in(2712, 2880):
            send_icon = os.path.join(self.conf_img_dir, "2880_bubble_circle_send_icon.png")
        elif height in (1280, ):
            send_icon = os.path.join(self.conf_img_dir, "1280_bubble_circle_send_icon.png")
        else:
            send_icon = os.path.join(self.conf_img_dir, "bubble_circle_send_icon.png")
        up_screen_path = os.path.join(g_resource['testcase_log_dir'], "swipe_up.png")
        down_screen_path = os.path.join(g_resource['testcase_log_dir'], "swipe_down.png")
        self._swipe_taking_screenshot(rate=0.6, screen_file_path=up_screen_path, direction='up')
        self._swipe_taking_screenshot(rate=0.4, screen_file_path=down_screen_path, direction='down')

        up_result = self.match_image(up_screen_path, send_icon, confidence=0.8)
        if up_result:
            g_logger.error("向上滑动时，显示了发布图标")
            ret = False
        down_result = self.match_image(down_screen_path, send_icon, confidence=0.8)
        if not down_result:
            g_logger.error("向下滑动时，没有找到发布图标")
            ret = False

        return ret

    def _swipe_taking_screenshot(self, rate=0.5, screen_file_path="", direction='up', duration=5):
        """
        滑动并截图
        Args:
            rate: 滑动比例
            direction: 滑动方向
            duration: 滑动时长
        """
        if not screen_file_path:
            screen_file_path = os.path.join(g_resource['testcase_log_dir'], "{}{}.png".format(direction, duration))
        _thread_swipe = IpeckerThread()
        _thread_swipe.start(self.device.swipe_screen, rate=rate, duration=duration, direction=direction)
        time.sleep(duration / 5)
        self.device.get_screenshot_as_file(screen_file_path)
        time.sleep(duration * 4 / 5 + 2)

    def check_bubble_circle_red_point(self):
        """
        检测游戏圈有更新是，显示小红点
        Returns:
            True: 检测成功， False: 检测失败
        """
        try:
            self.device.find_element_by_id(self.conf.gd_bubble_circle.id_red_point, timeout=10)
        except:
            g_logger.info("游戏圈没有新动态，未找到小红点")
            return True

        if self.into_bubble_circle_tab():
            try:
                self.device.find_element_by_id(self.conf.gd_bubble_circle.id_red_point, timeout=10)
                g_logger.error("游戏圈有更新，点击游戏圈后小红点还在")
                return False
            except:

                return True
        else:
            g_logger.error("进入游戏圈失败")
            return False

    def game_download_and_install(self, game_name, open_game=False, close_game=True, timeout=120):
        """
        游戏下载, 同一手机不能异步同时调用此方法，会导致包名和游戏名不匹配
         Args:
            game_name: 游戏名称，用于添加游戏映射
            open_game: 安装完成后是否打开游戏
            close_game: 是否关闭游戏， 需要open_game为True时才判断执行
            timeout: 安装超时
         Returns:
           True: 进入成功
           False：进入失败
         """
        if self.game_detail_download():
            return self.game_install(game_name, open_game=open_game, close_game=close_game, button_id=self.conf.gamecenter_game_download_installation.id, timeout=timeout)
        return False

    def get_gc_app(self):
        """
        点击畅玩更多按钮，下载游戏中心分发app
        Returns:
            True: 安装成功， False: 安装失败
        """
        try:
            g_logger.info("等待5秒，等待页面加载稳定")
            time.sleep(5)
            self.device.click_by_xpath(self.conf.gd_gc_app.xpath, desc="点击畅玩更多游戏", timeout=10)
            time.sleep(3)
            self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "点击畅玩更多游戏后截图.png"))
        except:
            return False
        if not self.game_install(game_name=self.conf.gd_gc_app.desc, open_game=False, confirm_guide=False, click_last_installed=False,
                                 button_xpath=self.conf.gd_gc_app.xpath, timeout=30):
            g_logger.warning("点击畅玩更多游戏后，游戏没有下载安装，回到游戏详情页重新点击")
            for i in range(20):
                self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
                time.sleep(2)
                try:
                    self.device.click_by_xpath(self.conf.gd_gc_app.xpath, desc="点击畅玩更多游戏", timeout=5)
                    time.sleep(3)
                    break
                except:
                    self.device.get_screenshot_as_file(os.path.join(g_resource['testcase_log_dir'], "未找到畅玩更多游戏按钮_{}.png".format(i+1)))
            else:
                return False
            return self.game_install(game_name=self.conf.gd_gc_app.desc, open_game=False, confirm_guide=False, timeout=30)
        else:
            return True

    def check_gc_app_display(self):
        """
        检测分发app按钮是否显示
        Returns:
            True: 显示， False: 没有显示
        """
        try:
            self.device.find_element_by_xpath(self.conf.gd_gc_app.xpath, timeout=10)
            g_logger.info("检测到畅玩更多游戏按钮")
            return True
        except:
            g_logger.info("未找到畅玩更多游戏按钮")
            return False
