# -*- coding: UTF-8 -*-

"""
File Name:      addUI
Author:         xumohan
Create Date:    2018/7/26
"""
from PyQt5.QtCore import *

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))