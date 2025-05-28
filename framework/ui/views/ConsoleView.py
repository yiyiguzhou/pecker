# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseView
Author:         zhangwei04
Create Date:    2018/10/11
"""
import os
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QMouseEvent

from framework.ui.widgets.ConsoleWidget import ConsoleWidget
from framework.core.resource import g_resource
from framework.utils.threads import IpeckerThread


class ConsoleView():
    def __init__(self, parent_laoyout):
        super().__init__()
        self.parent_laoyout = parent_laoyout
        self.layout = QVBoxLayout()
        self.parent_laoyout.addLayout(self.layout)
        self.console = ConsoleWidget()

    def init_UI(self):
        # button.setText("控制台")
        self.layout.addWidget(self.console)
        # self.start_thread()

    def start_thread(self):
        import threading
        th = threading.Thread(target=self.test_ping, args=())
        th.start()

    def test_ping(self):
        import time
        import sys
        from subprocess import Popen, PIPE
        start_time = time.time()
        while time.time() - start_time < 1000:
            with Popen("ping 127.0.0.1 -n 20", stdout=PIPE) as fp:
                # out, err = fp.communicate()
                for line in iter(fp.stdout.readline, b''):
                    try:
                        print(line.decode('gbk'))
                    except Exception as e:
                        pass

        print("执行结束")


