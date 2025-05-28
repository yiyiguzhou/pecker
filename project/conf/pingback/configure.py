# -*- coding: UTF-8 -*-

"""
File Name:      configure
Author:         zhangwei04
Create Date:    2018/5/18
"""
import os
import configparser

g_conf = configparser.ConfigParser()
g_conf.read(os.path.join(os.path.dirname(__file__), 'conf.ini'), encoding='utf-8')

