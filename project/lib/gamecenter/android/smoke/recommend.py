# -*- coding: UTF-8 -*-

"""
File Name:      recommend
Author:         zhangwei04
Create Date:    2018/11/12
"""
import time

from project.lib.gamecenter.android.smoke.common import Common, g_logger


class Recommend(Common):
    """推荐页"""
    def __init__(self, target, ele_conf_name='android'):
        super().__init__(target=target, ele_conf_name=ele_conf_name)
        # self.target = target
        # self.data = target.data
        # self.device = target.device

    def into_focus_detail_page(self, title):
        """进入焦点图
        Args:
            title: 标题参数,用于进入对应标题的焦点图
        """
        ele = self.device.swipe_ele_find_ele(swipe_id="com.qiyi.gamecenter:id/bannerContainer", find_xpath=self.conf.gc_recommend_focus.xpath_title.format(title),
                                      rate=0.8, timeout=120, direction="right")
        if ele:
            ele.click()
            time.sleep(3)
            return True
        else:
            g_logger.error("焦点图查找：{}失败".format(title))
            return False
