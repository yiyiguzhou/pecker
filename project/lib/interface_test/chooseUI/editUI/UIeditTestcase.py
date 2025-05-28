# -*- coding: UTF-8 -*-

"""
File Name:      UIeditTestcase
Author:         xumohan
Create Date:    2018/7/31
"""
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from project.lib.interface_test.chooseUI import UIEmittingStream as ue, run_temp_interface as rti
from project.lib.interface_test.chooseUI.editUI import edit_testcase as et, save_new_testcase_xml as sntx
from framework.logger.logger import g_logger
from framework.main import start


class edit_Testcase(QWidget):
    def __init__(self, line_list):
        super().__init__()
        self.line_list = line_list
        #self.initUI(self.line_list)

    def initUI(self, line_list):

        # 编辑用例部分
        self.edit_part = QTreeWidget()
        self.edit_part.clear()
        self.edit_part.setColumnCount(2)
        self.edit_part.setColumnWidth(0,240)
        self.edit_part.setMaximumWidth(480)
        self.edit_part.setMinimumWidth(480)
        self.edit_part.setMaximumHeight(459)
        self.edit_part.setMinimumHeight(459)
        edit_part_parent = QTreeWidgetItem(self.edit_part)
        edit_part_parent.setText(0, "所有用例")
        testcases_dict = self.get_edit_testcase_dict(line_list)[0]
        self.file_path = self.get_edit_testcase_dict(line_list)[1]
        self.set_all_testcases(testcases_dict, edit_part_parent)
        self.edit_part.expandToDepth(2)


        # 保存按钮
        self.save_edit_button = QPushButton(self)
        self.save_edit_button.setObjectName("save_edit_button")
        self.save_edit_button.setText("Save")
        self.save_edit_button.clicked.connect(self.save_edit_testcase)

        # 测试按钮
        self.test_button = QPushButton(self)
        self.test_button.setObjectName("test_button")
        self.test_button.setText("Test")
        self.test_button.clicked.connect(self.test_edit_testcase)

        # 退出按钮
        self.quit_button = QPushButton(self)
        self.quit_button.setObjectName("quit_button")
        self.quit_button.setText("Quit")
        self.quit_button.clicked.connect(self.quit_window)

        #控制台
        self.terminal_head = QLabel(self)
        self.terminal_head.setText("控制台输出：")
        self.terminal_text = QTextEdit(self)
        self.terminal_text.setReadOnly(True)
        self.terminal_text.setMaximumWidth(280)
        self.terminal_text.setMinimumWidth(280)
        self.terminal_text.setMaximumHeight(370)
        self.terminal_text.setMinimumHeight(370)
        sys.stdout = ue.EmittingStream(textWritten=self.normal_output_written)
        sys.stder = ue.EmittingStream(textWritten=self.normal_output_written)
        g_logger.set_ui_console(self)

        # 结果显示区域
        self.result_show_part = QTextEdit(self)
        self.result_show_part.setReadOnly(True)
        self.result_show_part.setAlignment(Qt.AlignHCenter)
        self.result_show_part.setMaximumWidth(280)
        self.result_show_part.setMinimumWidth(280)
        self.result_show_part.setMaximumHeight(100)
        self.result_show_part.setMinimumHeight(100)

        # 左中右三个大布局
        self.total_layout = QHBoxLayout(self)
        self.middle_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        # 中间区域编辑界面&按钮
        self.testcase_edit_layout = QHBoxLayout()
        self.testcase_edit_button_layout = QHBoxLayout()


        # 添加控件
        self.testcase_edit_layout.addWidget(self.edit_part)
        self.testcase_edit_button_layout.addWidget(self.save_edit_button)
        self.testcase_edit_button_layout.addWidget(self.test_button)
        self.testcase_edit_button_layout.addWidget(self.quit_button)
        self.right_layout.addWidget(self.terminal_head)
        self.right_layout.addWidget(self.terminal_text)
        self.right_layout.addWidget(self.result_show_part)

        # 加到全局布局
        self.middle_layout.addLayout(self.testcase_edit_layout)
        self.middle_layout.addLayout(self.testcase_edit_button_layout)
        self.total_layout.addLayout(self.middle_layout)
        self.total_layout.addLayout(self.right_layout)

        # 整个界面
        self.setGeometry(400, 200, 800, 500)
        self.setWindowTitle('Testcases')
        self.show()

    def get_testcase_dict(self, item, item_dict):
        if not item.childCount() == 0:
            item_dict[item.text(0)] = {}
            for i in range(item.childCount()):
                self.get_testcase_dict(item.child(i), item_dict[item.text(0)])
        else:
            item_dict[item.text(0)] = item.text(1)
        return item_dict

    def change_edit_testcase_content(self, item_dict):
        item_dict = item_dict["所有用例"]
        temp_part_testcase_dict = item_dict["suite"]["testcase"]
        temp_part_testcase_list = []
        for itd in temp_part_testcase_dict.keys():
            temp_part_testcase_list.append(temp_part_testcase_dict[itd])
        if len(temp_part_testcase_list) == 1:
            item_dict["suite"]["testcase"] = temp_part_testcase_list[0]
        else:
            item_dict["suite"]["testcase"] = temp_part_testcase_list
        return item_dict

    def save_edit_testcase(self):
        # 保存修改的部分
        test_case_item_dict = self.get_testcase_dict(self.edit_part.topLevelItem(0), {})
        test_case_item_dict = self.change_edit_testcase_content(test_case_item_dict)
        # 这里写把字典写成新xml, 此xml转换暂时只支持非data部分
        sntx.save_edit_xml(test_case_item_dict, self.file_path)
        #print("total_line_list", test_case_item_dict)

    def test_edit_testcase(self):
        # 测试修改的部分

        rti.run_temp_interface(self.total_line_list)
        start()

    def normal_output_written(self, text):
        cursor = self.terminal_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.terminal_text.setTextCursor(cursor)
        self.terminal_text.ensureCursorVisible()

    def quit_window(self):
        self.close()


    def set_all_testcases(self, testcases_dict, new_parent):
        if isinstance(testcases_dict, dict):
            for d in testcases_dict.keys():
                if not d == "testcase":
                    next_parent = QTreeWidgetItem(new_parent)
                    next_parent.setText(0, d)
                    next_parent.setFlags(next_parent.flags() | Qt.ItemIsEditable)
                    self.set_all_testcases(testcases_dict[d], next_parent)
                else:
                    if not isinstance(testcases_dict[d], list):
                        next_parent = QTreeWidgetItem(new_parent)
                        next_parent.setText(0, d)
                        next_parent.setFlags(next_parent.flags() | Qt.ItemIsEditable)
                        self.set_all_testcases(testcases_dict[d], next_parent)
                    else:
                        next_parent = QTreeWidgetItem(new_parent)
                        next_parent.setText(0, d)
                        for test_case in testcases_dict[d]:
                            next_testcase_parent = QTreeWidgetItem(next_parent)
                            next_testcase_parent_title = str(test_case["id"]) + " " + str(test_case["name"])
                            next_testcase_parent.setText(0, next_testcase_parent_title)
                            next_testcase_parent.setFlags(next_testcase_parent.flags())
                            self.set_all_testcases(test_case, next_testcase_parent)

        elif isinstance(testcases_dict, list):
            for l in testcases_dict:
                self.set_all_testcases(l, new_parent)
        else:
            new_parent.setText(1, testcases_dict)

    def get_edit_testcase_dict(self, line_list):
        path = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        testcases_path = os.path.join(path, "script")
        testcases_dict, file_path = et.test_case_xml_to_dict(line_list, testcases_path)
        return testcases_dict, file_path

def edit_testcase(line_list):
    app = QApplication(sys.argv)
    ex = edit_Testcase(line_list)
    sys.exit(app.exec_())

"""
line_list = ['UGameList_listByGameOnlineDate.py', 'testaa', 'interface_test']
edit_testcase(line_list)
"""