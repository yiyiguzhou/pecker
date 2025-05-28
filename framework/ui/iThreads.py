# -*- coding: UTF-8 -*-

"""
File Name:      thread
Author:         zhangwei04
Create Date:    2018/10/29
"""
import threading
from PyQt5.QtCore import *


class iPeckerThread(QThread):
    """ipecker框架执行线程类"""
    def __init__(self, dispatch):
        super().__init__()
        self.dispatch = dispatch
        self._thread = threading.Thread(target=self._start, args=())

    def start(self, priority=None):
        """启动框架线程"""
        self._thread.start()

    def _start(self):
        """线程回调函数"""
        self.dispatch.start()
