"""
File Name:      update
Author:         xuxiaofang_sx
Create Date:    2018/9/5
"""

import os
import time
from framework.logger.logger import g_logger
from framework.core.resource import g_resource
from project.lib.android import Android
from project.lib.sdk.android.mainland.mainland import Mainland


class  Upadte(Mainland):
    def __init__(self, target):
        super().__init__(target=target, ele_conf_name='android_sdk')

        self.target = target
        self.data = target.data
        self.device = target.device

    def  force_update_interface(self):
        """
        进入游戏-强制更新页面显示
        Args:
            game_text: 更新界面显示
        Returns:
            True: 更新成功
            False：更新失败
        """
        try:
            self.device.find_element_by_xpath("//android.widget.TextView[@text='有新版本需要更新']")
            time.sleep(5)
        except Exception as e:
            return False
        return True

    def force_update(self):
        """
        进入游戏-强制更新页面显示-强制更新成功
        Args:
            game_text: 更新界面显示
        Returns:
            True: 更新成功
            False：更新失败
        """
        try:

            self.device.find_element_by_id(self.conf.confirm_update.id, timeout=5).click()
            time.sleep(5)
        except Exception as e:
            return False
        return True

    def silent_update(self):
        """
        进入游戏-静默更新成功
        Args:
            game_text: 更新界面显示
        Returns:
            True: 更新成功
            False：更新失败
        """
        try:
            #静默更新成功
            self.device.find_element_by_id(self.conf.confirm_update.id, timeout=5).click()
            time.sleep(5)
        except Exception as e:
            return False
        return True