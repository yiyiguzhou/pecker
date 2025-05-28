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
from .login import login
from .intogame import intogame


class h5sdk(login, intogame):

    def __init__(self, target):
        """
        :type target: object
        """

        self.target = target
        self.data = target.data
        self.device = target.device