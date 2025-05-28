# -*- coding: UTF-8 -*-

"""
File Name:      BaseApi
Author:         zhangwei04
Create Date:    2018/5/14
"""
import os
import time
from project.conf.elements_conf.configure import ElementConfig
from framework.logger.logger import g_logger
# from framework.utils.iMitmProxy.imitm import IMitm


class BaseInterface(object):
    def __init__(self, target, ele_conf_name=None):
        self.target = target
        self.data = target.data
        self.device = target.device if target else None
        self.conf = None
        self.get_config(ele_conf_name)
        # self.imitm = IMitm()

    def get_config(self, ele_conf_name):
        """读取配置信息
        Args:
            ele_conf_name: 配置文件名称，默认配置在project/conf目录下
        """
        if not ele_conf_name:
            mobile_type = self.device.data.get("type", None)
            if not mobile_type:
                g_logger.warning("element config file not parsed, since device aml config file have not find type element")
        else:
            mobile_type = ele_conf_name
        self.conf = ElementConfig(mobile_type)

    def click_from_position(self, x_rate, y_rate, sleep_time=2):
        """通过坐标点击
        Args:
            x_rate: 若x_rate大于1，则表示绝对坐标点，否者为位置比例
            y_rate: 若y_rate大于1，则表示绝对坐标点，否者为位置比例
        """
        if x_rate > 1 and y_rate > 1:
            pos = (x_rate, y_rate)
        else:
            size = self.device.get_window_size()
            width = size.get('width')
            height = size.get('height')
            pos = (x_rate if x_rate > 1 else width * x_rate, y_rate if y_rate > 1 else height * y_rate)

        self.device.adb.tap([pos], duration=50)
        time.sleep(sleep_time)

    @staticmethod
    def match_image(src_img_path: str, des_img_path: str, confidence=0.5, timeout=2):
        """图像匹配
        Args:
            src_img_path: 原图像，即匹配时的全局图片，绝大多数情况下是手机截图
            des_img_path: 目标图片，即匹配时的是否满足的部分图片
            confidence: 相似度阈值
        Returns:
            True: 匹配成功
            False： 出现异常或者匹配失败
        """
        # 判断文件路径是否存在
        if not os.path.exists(src_img_path) or not os.path.exists(des_img_path):
            g_logger.error("文件{}\n {}\n不存在，请检测文件是否存在".format(src_img_path, des_img_path))
            return None

        # try:
        #     from PIL import Image
        # except:
        #     g_logger.error("Pillow 库没有安装，请使用命令：pip install Pillow进行安装")
        #     return None
        # src_img = Image.open(src_img_path)
        # des_img = Image.open(des_img_path)
        # if src_img.width < des_img.width or src_img.height < des_img.height:
        #     return None

        try:
            import aircv as ac
        except:
            g_logger.error("aircv 库没有安装，请使用命令：pip install aircv进行安装")
            return None

        src_img_obj = ac.imread(src_img_path)
        des_img_obj = ac.imread(des_img_path)
        if src_img_obj.shape[0] < des_img_obj.shape[0] or src_img_obj.shape[1] < des_img_obj.shape[1]:
            g_logger.info("原图片尺寸小于目标图片尺寸，原图片：{}，目标图片：{}".format(src_img_path, des_img_path))
            return None
        try:
            match_result = ac.find_template(src_img_obj, des_img_obj, confidence)
        except Exception as e:
            g_logger.error(str(e))
            return None

        return match_result

