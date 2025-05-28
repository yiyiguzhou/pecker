# -*- coding: UTF-8 -*-

"""
File Name:      GUI
Author:         xumohan
Create Date:    2018/7/23
"""

import sys
from PyQt5.QtWidgets import *
from project.lib.interface_test.UI import transfer_excel_to_xml as etx


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 选择文件
        choose_file_button = QPushButton(self)
        choose_file_button.setText("Choose a file")
        choose_file_button.clicked.connect(self.choose_file)

        self.show_filename_label = QLabel(self)
        self.input_filename_textbox = QLineEdit(self)

        submit_button = QPushButton(self)
        submit_button.setText("Submit")
        submit_button.clicked.connect(self.beginTest)

        self.input_filename_textbox.move(20, 40)
        choose_file_button.move(180, 40)
        self.show_filename_label.move(20, 80)
        submit_button.move(300, 40)
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

    def beginTest(self):
        input_file_name = self.input_filename_textbox.text()
        print("text: ", input_file_name)
        etx.excel_to_xml(input_file_name,"testUI")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())