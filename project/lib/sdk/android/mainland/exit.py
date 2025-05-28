"""
File Name:      game_exit_guide
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""
import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from project.lib.sdk.android.mainland.mainland import Mainland

class  Exit(Mainland):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')

        self.target = target
        self.data = target.data
        self.device = target.device

    def test(self):
        """
        daluDemo测试接口
        """
        # self.device.test()
        g_logger.info("Demoapk test")

    def game_out(self):
        """
        退出游戏

        Returns:
            True: 退出成功
            False：退出失败
        """
        size = self.device.get_window_size()
        width = size.get('width')
        height = size.get('height')

        # 滑动查找退出游戏
        for i in range(10):
            try:
                self.device.find_element_by_xpath("//android.widget.Button[@text='游戏退出']").click()
                time.sleep(2)
                break
            except:
                if i == 9:
                    return False

                self.device.swipe(width / 2, height * 3 / 4, width / 2, height * 1 / 4)
                time.sleep(1)

                continue
        #立即退出游戏
        try:
            self.device.find_element_by_id(self.conf.out2_game.id, timeout=5).click()
            time.sleep(5)
        except:
            return False
        return True

    def mobile_phone_return2(self):
        """
        进入游戏-手机物理键退出游戏
        Returns:
            True: 退出游戏成功
            False：退出游戏失败
        """
        try:
            self.device.adb.adb_shell("input keyevent KEYCODE_BACK ")
            time.sleep(5)
            self.device.find_element_by_id(self.conf.out2_game.id, timeout=5).click()
            time.sleep(5)
        except:
            return False
        return True

