# -*- coding: UTF-8 -*-

"""
File Name:      intogame
Author:         fuhongzi
Create Date:    2018/5/9
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource


class intogame(object):

    def __init__(self, target):
        self.target = target
        self.data = target.data
        self.device = target.device

    """
           进入棋牌游戏
           Returns:
               True: 进入成功
               False：进入失败
    """
    def into_cardgame(self, game_text=''):
        time.sleep(3)
        try:
            self.device.find_element_by_id('com.qiyi.gamecenter:id/detail_go_h5game_btn',timeout=3).click()
        except:
            g_logger.error('into card game failed:'+ game_text)
            return False
        return True
    """
        进入非棋牌游戏
        Returns:
            True: 进入成功
            False：进入失败
    """
    def into_h5game(self, game_text=''):
        time.sleep(3)
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='点击即玩']").click()
        except:
            g_logger.error('into h5 game failed:' + game_text)
            return False
        return True
    """
        清除缓存
        Returns:
            True: 清除成功
            False：清除失败
    """
    def no_cache(self):
        time.sleep(3)
        self.device.adb.clear_app_data("com.qiyi.video")
        self.device.launch_app()
        try:
            self.device.find_element_by_id('com.qiyi.video:id/navi0', timeout=5).click()
            g_logger.info('11')
            time.sleep(2)
            self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏中心']").click()
            time.sleep(2)
            g_logger.info('22')
            self.device.find_element_by_id('com.qiyi.video:id/qyplugin_install_dialog_ok_btn', timeout=3).click()
            g_logger.info('33')
            time.sleep(15)
        except:
            g_logger.error('clear cache fail ')
            return False
        return True

    def into_gamecenter(self):
        """
        从推荐页面中基线进入游戏
        Returns:
            True：进入成功
            False：进入失败
        """
        ret = False
        time.sleep(6)
        for i in range(3):
            try:
                self.device.find_element_by_id('com.qiyi.video:id/navi0', timeout=5).click()
                time.sleep(2)
                self.device.find_element_by_xpath("//android.widget.TextView[@text='游戏中心']").click()
                time.sleep(2)
                break
            except Exception as e:
                g_logger.info(str(e))
                # 升级提示
                try:
                    self.device.find_element_by_id('com.qiyi.video:id/smart_upgrade_close', timeout=3).click()
                    time.sleep(1)
                except:
                    pass
                if i == 2:
                    g_logger.error("into gamecenter failed")
                    self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'],
                                                                    "into_game_center_{}_failed.png".format(
                                                                        g_resource['testcase_loop'])))
                    return False
                time.sleep(3)

        try:
            ele = self.device.find_element_by_id('com.qiyi.gamecenter:id/actionBar_title', timeout=6)
            if '游戏中心' not in ele.get_attribute('text'):
                self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'],
                                                                "into_game_center_{}_failed.png".format(
                                                                    g_resource['testcase_loop'])))
                return False
        except:
            self.device.adb.screen_shot(os.path.join(g_resource['testcase_log_dir'],
                                                            "into_game_center_{}_failed.png".format(
                                                                time.ctime().replace(':', '_'))))
            return False

        return True

    def gamecenter_search(self, search_text=''):
        """
        游戏中心页面搜索操作
        Args:
            search_text: 搜索文本
        Returns:
            True: 搜索成功
            False: 搜索失败
        """
        time.sleep(3)
        try:
            time.sleep(1)
            self.device.find_element_by_id('com.qiyi.gamecenter:id/ppsgame_search_action_bar_et_search').send_keys(
                search_text)
            time.sleep(2)
            self.device.hide_keyboard()
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(search_text), timeout=10)
        except Exception as e:
            return False
        return True

    def into_gamedetail(self, game_text=''):
        """
        游戏中心-进入游戏详情界面
        Args:
            game_text: 进入的游戏名
        Returns:
            True: 进入成功
            False：进入失败
        """
        time.sleep(3)
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='{}']".format(game_text)).click()
        except:
            g_logger.info('into game：{} failed'.format(game_text))
            return False
        return True