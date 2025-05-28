# -*- coding: UTF-8 -*-

"""
File Name:      __init__.py
Author:         zhangwei04
Create Date:    2017/12/22
"""
import os
import sys
import time
from framework.core.resource import g_resource


def _create_log_dir():
    """
    创建日志目录
    """
    time_format = time.strftime("%m-%d_%H_%M_%S", time.localtime(g_resource['start_time']))
    g_resource['log_path'] = os.path.abspath(os.path.join(g_resource['project_path'], 'result', time_format))
    if not os.path.exists(g_resource['log_path']):
        os.makedirs(g_resource['log_path'])


g_resource['framework_path'] = os.path.dirname(__file__)
g_resource['project_path'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'project'))
g_resource['start_time'] = time.time()

_create_log_dir()
