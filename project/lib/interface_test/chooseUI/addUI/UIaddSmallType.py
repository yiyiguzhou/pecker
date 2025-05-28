# -*- coding: UTF-8 -*-

"""
File Name:      addSmallType
Author:         xumohan
Create Date:    2018/7/30
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from project.lib.interface_test.chooseUI.addUI import add_new_content as anc
from project.lib.interface_test.chooseUI import UImain


class UIaddSmallType(QWidget):
    def __init__(self, test_group):
        super().__init__()
        self.test_group = test_group
        self.new_small_type = ""

        #self.initUI()

    def initUI(self):
        print(self.test_group)
        self.show_add_label = QLabel(self)
        input_new_type = QLineEdit(self)

        input_new_type.move(60, 90)
        self.show_add_label.move(60, 40)
        self.show_add_label.clear()
        previous_text = "业务线： " + self.test_group + "\n新增文件夹： "
        self.show_add_label.setText(previous_text)

        input_new_type.textChanged[str].connect(self.show_new_type)

        self.submit_button = QPushButton('submit', self)
        self.submit_button.move(190,120)
        self.submit_button.clicked.connect(self.submit_new_type)
        #self.submit_button.clicked.connect(QCoreApplication.quit)
        self.submit_button.clicked.connect(self.quit_new_window)

        self.setGeometry(500, 400, 280, 170)
        self.setWindowTitle('新增文件夹')
        self.show()

    def show_new_type(self, text):
        self.new_small_type = text
        new_text = "业务线： " + self.test_group +"\n新增文件夹： " + self.new_small_type
        self.show_add_label.setText(new_text)
        self.show_add_label.adjustSize()

    def submit_new_type(self):
        print("tianjiala")
        self.show_add_label.clear()
        anc.add_new_type(self.test_group, self.new_small_type)

    def quit_new_window(self):
        self.close()


def add_small_new_type(test_group):
    app = QApplication(sys.argv)
    ex = UIaddSmallType(test_group)
    sys.exit(app.exec_())


# test_group = "interface_test"
# add_small_new_type(test_group)