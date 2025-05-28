# -*- coding: UTF-8 -*-

"""
File Name:      configure
Author:         zhangwei04
Create Date:    2018/5/18
"""
import os
import time
import configparser
from framework.logger.logger import g_logger


class ElementConfig(object):
    def __init__(self, mobile_type):
        """
        初始化配置类
        business_line: 业务线
        move_end: 移动端
        """
        self._sections = list()
        self.__file_path = "{}.conf".format(mobile_type.lower())
        self.__read_conf()

    def __read_conf(self):
        file_path = os.path.join(os.path.dirname(__file__), self.__file_path)
        conf = configparser.ConfigParser()
        with open(file_path, "r", encoding='utf-8') as fp:
            conf.read_file(fp)
            for section in conf.sections():
                self.__add_nodes(section, conf)

    def __add_nodes(self, section, conf):
        if not hasattr(self, section):
            self._sections.append(section)
            self.__setattr__(section, self.ElementNode(section, conf))

    def get(self, section, node_key):
        try:
            value = getattr(getattr(self, section), node_key)
            return value
        except:
            g_logger.warning("section:{}未找到key:{}".format(section, node_key))
            return None

    class ElementNode(object):
        def __init__(self, section, conf):
            self.__add_key(section, conf)

        def __add_key(self, section, conf):
            for opt in conf.options(section):
                self.__setattr__(opt, conf.get(section, opt))


class AccountConfig(ElementConfig):
    def __init__(self, conf_name="account"):
        """
        初始化账号配置类
        business_line: 业务线
        move_end: 移动端
        """
        super().__init__(conf_name)

    def check_available(self, section):
        """
        检测账号是否可用
        Args:
            section: section
        Returns:
            True: 账号处于可用期，False: 账号失效
        """
        try:
            node = self.__getattribute__(section)
            try:    # 检测账号是否是无限期
                dead_time_str = node.dead_time
            except:
                g_logger.info("账号{}未配置使用期, 默认为无限期".format(node.username))
                return True

            time_dead = int(time.mktime(time.strptime(dead_time_str, "%Y-%m-%d %H:%M")))
            if time_dead < time.time():
                g_logger.warning("账号已失效，失效日期为: {}".format(dead_time_str))
                return False
        except Exception as e:
            return False

        return True


if __name__ == "__main__":
    # conf = ElementConfig("android")
    # v = conf.base_my_login_phone_num.desc
    # print(conf.base_my_login_phone_num.desc)
    # v = conf.base_my_login_phone_num.cls
    # print(conf.base_my_login_phone_num.cls)
    # print(conf.base_my_login_phone_num.id)
    #
    # app_conf = ElementConfig("game")
    # print(app_conf.get("爱奇艺麻将", "package"))
    #
    account = AccountConfig()
    ret = account.check_available("platform_1")
    print(ret)
