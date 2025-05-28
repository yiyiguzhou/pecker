# -*- coding: UTF-8 -*-

"""
File Name:      layout
Author:         zhangwei04
Create Date:    2018/10/10
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QTextCursor

from framework.ui.views.TestCaseAndConfView import TestCaseAndConfView
from framework.ui.views.ConsoleView import ConsoleView
from framework.ui.views.TestCaseRunStatusView import TestCaseRunStatusView
from framework.ui.Adapter import Adapter
from framework.ui.signal.Signal import g_signal

from framework.logger.logger import g_logger, g_framework_logger


class OutStream(QtCore.QObject):
    """打印重定向类"""
    text_written = QtCore.pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(text)


class MainForm(QWidget):
    """UI入口类，生成总体布局列实例，适配器实例"""
    def __init__(self):
        super().__init__()
        g_signal.is_use_ui.connect(self._is_use_ui)
        g_signal.ui_print[str].connect(self.normal_output_written)

        self.setWindowTitle('ipecker')
        self.resize(1200, 800)
        self.layout = QHBoxLayout()     # 主布局
        self.testcase_and_conf_view = TestCaseAndConfView(self.layout)
        self.tetcase_console_view = ConsoleView(self.layout)
        self.testcase_run_status_view = TestCaseRunStatusView(self.layout)
        self.adapter = Adapter()

        self.testcase_and_conf_view.init_UI()
        self.tetcase_console_view.init_UI()
        self.testcase_run_status_view.init_UI()
        self.setLayout(self.layout)
        sys.stdout = OutStream(text_written=self.normal_output_written)

        g_logger.set_ui_console(self)
        g_framework_logger.set_ui_console(self)

        g_signal.use_ui.emit(True)

    def __del__(self):
        if sys:
            sys.stdout = sys.__stdout__

    def normal_output_written(self, text):
        """打印重定向回调函数"""
        try:
            console = self.tetcase_console_view.console

            cursor = console.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(text)
            console.setTextCursor(cursor)
            console.ensureCursorVisible()
        except Exception as e:
            pass

    def _is_use_ui(self):
        """是否UI信号发射函数"""
        g_signal.use_ui.emit(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mf = MainForm()
    mf.show()
    sys.exit(app.exec_())
