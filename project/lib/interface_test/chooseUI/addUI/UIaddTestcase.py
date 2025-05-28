# -*- coding: UTF-8 -*-

"""
File Name:      GUI
Author:         xumohan
Create Date:    2018/7/23
"""

import sys
from PyQt5.QtWidgets import *
from project.lib.interface_test.chooseUI.addUI import transfer_excel_to_xml as etx
from project.lib.interface_test.chooseUI import write_new_py


class add_new_testcase_window(QWidget):
    def __init__(self, line_list):
        super().__init__()

        self.line_list = line_list
        #self.initUI()

    def initUI(self):
        # 选择文件
        choose_file_button = QPushButton(self)
        choose_file_button.setText("Choose a file")
        choose_file_button.clicked.connect(self.choose_file)

        self.show_filename_label = QLabel(self)
        self.input_filename_textbox = QLineEdit(self)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.change_excel_to_xml)
        self.submit_button.clicked.connect(self.quit_window)

        self.input_filename_textbox.move(20, 40)
        choose_file_button.move(180, 40)
        self.show_filename_label.move(20, 80)
        self.submit_button.move(300, 40)
        self.input_filename_textbox.textChanged[str].connect(self.show_filename_label_onChanged)

        self.setGeometry(400, 400, 400, 300)
        self.setWindowTitle('QLineEdit')
        self.show()

    def show_filename_label_onChanged(self, text):
        self.show_filename_label.setText(text)
        self.show_filename_label.adjustSize()

    def choose_file(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "C:/",
                                                          "All Files (*);;Text Files (*.txt);;Xlsx Files (*.xlsx)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(fileName1)

        self.input_filename_textbox.setText(fileName1)
        self.input_filename_textbox.adjustSize()

        """
        files, ok1 = QFileDialog.getOpenFileNames(self,
                                                  "多文件选择",
                                                  "C:/",
                                                  "All Files (*);;Text Files (*.txt)")
        print(files, ok1)
        """

    def change_excel_to_xml(self):
        input_file_name = self.input_filename_textbox.text()
        print("text: ", input_file_name)
        file_name = etx.excel_to_xml(input_file_name, self.line_list)
        write_new_py.write_new_py_file(file_name)

    def quit_window(self):
        self.close()


def add_test_case(line_list):
    app = QApplication(sys.argv)
    ex = add_new_testcase_window(line_list)
    sys.exit(app.exec_())