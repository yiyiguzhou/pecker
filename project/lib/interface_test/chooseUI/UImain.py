# -*- coding: UTF-8 -*-

"""
File Name:      chooseUImain
Author:         xumohan
Create Date:    2018/7/23
"""
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from project.lib.interface_test.chooseUI import check_all_files as caf, UIEmittingStream as ue, run_temp_interface as rti
from framework.main import start
from project.lib.interface_test.chooseUI.addUI import UIaddSmallType, UIaddTestcase
from project.lib.interface_test.chooseUI.editUI import UIeditTestcase
from framework.logger.logger import g_logger

class Choose_testcase(QWidget):

    def __init__(self, choice_list):
        super().__init__()
        self.checkbox_list = []
        self.testcase_list = []
        self.total_line_list = []
        self.myControls = {}
        self.first_list_name = ""
        self.second_list_name = ""
        self.choice_list = choice_list
        #self.ui_edit_testcase = UIeditTestcase.edit_Testcase([])
        self.initUI(self.choice_list)

    def initUI(self, choice_list):
        # show_choice_label显示选择的测试用例的结果
        self.choice_result_head = QLabel(self)
        self.choice_result_head.setText("已选择的用例：")
        self.show_choice_label = QTextEdit(self)
        self.show_choice_label.setReadOnly(True)
        self.show_choice_label.setAlignment(Qt.AlignHCenter)
        self.show_choice_label.setMaximumWidth(230)
        self.show_choice_label.setMinimumWidth(230)
        self.show_choice_label.setMaximumHeight(410)
        self.show_choice_label.setMinimumHeight(410)


        # 添加下拉框,total_type_combo,大类型选择
        self.total_type_combo = QComboBox(self)
        for c in choice_list:
            self.total_type_combo.addItem(c)
        self.total_type_combo.activated[str].connect(self.get_all_testcases)
        self.total_type_combo.activated[str].connect(self.get_all_small_types)

        # 添加下拉框,small_types_combo,二級菜单
        self.small_types_combo = QComboBox(self)

        # 用例结果显示树
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setMaximumWidth(280)
        self.tree.setMinimumWidth(280)
        self.tree.setMaximumHeight(459)
        self.tree.setMinimumHeight(459)
        self.tree.doubleClicked.connect(self.get_edit_testcase_content)

        # 控制台输出窗口
        self.terminal_head = QLabel(self)
        self.terminal_head.setText("控制台输出：")
        self.terminal_text = QTextEdit(self)
        self.terminal_text.setReadOnly(True)
        self.terminal_text.setMaximumWidth(280)
        self.terminal_text.setMinimumWidth(280)
        self.terminal_text.setMaximumHeight(466)
        self.terminal_text.setMinimumHeight(466)
        sys.stdout = ue.EmittingStream(textWritten=self.normal_output_written)
        sys.stder = ue.EmittingStream(textWritten=self.normal_output_written)
        g_logger.set_ui_console(self)

        # 提交按钮
        self.submit_button = QPushButton(self)
        self.submit_button.setObjectName("submit_button")
        self.submit_button.setText("Begin Test")
        self.submit_button.clicked.connect(self.run_test_case)

        # 导出用例按钮
        self.export_usecase = QPushButton(self)
        self.export_usecase.setObjectName("export_usecase")
        self.export_usecase.setText("Export Usecase")
        self.export_usecase.clicked.connect(self.export_usecase_method)


        #添加新用例按钮
        self.add_new_testcase_button = QPushButton(self)
        self.add_new_testcase_button.setObjectName("add_new_testcase_button")
        self.add_new_testcase_button.setText("Add new testcase")
        self.add_new_testcase_button.clicked.connect(self.add_new_testcase)

        # 关闭窗口按钮
        self.close_button = QPushButton(self)
        self.close_button.setObjectName("close_button")
        self.close_button.setText("Close")
        self.close_button.clicked.connect(self.close_window)

        # 运行状态区域
        self.state_text = QTextEdit(self)
        self.state_text.setReadOnly(True)
        self.state_text.setMaximumWidth(280)
        self.state_text.setMinimumWidth(280)
        self.state_text.setMaximumHeight(459)
        self.state_text.setMinimumHeight(459)
        self.state_text.setText("这里以后显示运行状态、结果")


        # 全局布局， 左中右三个区域
        self.total_layout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.middle_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        # 左局部布局
        self.choose_layout = QHBoxLayout() # 选择区域，选择一级下拉菜单，二级下拉菜单，添加新用例
        self.choose_layout.SetMaximumSize = 200
        self.testcase_tree_layout = QHBoxLayout() # 用例显示区域，用例树+选择结果显示
        self.tree_layout = QHBoxLayout() # 用例树区域
        self.choice_result_layout = QVBoxLayout() # 选择结果显示区域
        self.show_result_layout = QVBoxLayout()
        self.show_result_button_layout = QHBoxLayout()
        self.choice_result_layout.addLayout(self.show_result_layout)
        self.choice_result_layout.addLayout(self.show_result_button_layout)
        self.testcase_tree_layout.addLayout(self.tree_layout)
        self.testcase_tree_layout.addLayout(self.choice_result_layout)
        self.left_layout.addLayout(self.choose_layout, 1)
        self.left_layout.addLayout(self.testcase_tree_layout, 1)

        # 右局部布局
        self.state_layout = QHBoxLayout()
        self.quit_layout = QVBoxLayout()
        self.right_layout.addLayout(self.state_layout)
        self.right_layout.addLayout(self.quit_layout)

        # 这里向局部布局内添加部件
        self.choose_layout.addWidget(self.total_type_combo)
        self.choose_layout.addWidget(self.small_types_combo)
        self.choose_layout.addWidget(self.add_new_testcase_button)
        self.middle_layout.addWidget(self.terminal_head)
        self.middle_layout.addWidget(self.terminal_text)
        self.quit_layout.addWidget(self.close_button)
        self.tree_layout.addWidget(self.tree)
        self.show_result_layout.addWidget(self.choice_result_head)
        self.show_result_layout.addWidget(self.show_choice_label)
        self.show_result_button_layout.addWidget(self.export_usecase)
        self.show_result_button_layout.addWidget(self.submit_button)
        self.state_layout.addWidget(self.state_text)


        # 加到全局布局
        self.total_layout.addLayout(self.left_layout)
        self.total_layout.addLayout(self.middle_layout)
        self.total_layout.addLayout(self.right_layout)

        self.setGeometry(300, 200, 1200, 500)
        self.setWindowTitle('Testcases')
        self.show()

    def get_edit_testcase_content(self):
        current_text_line_list = self.get_all_line_of_item(self.tree.currentItem(), [])
        if not self.second_list_name == "":
            current_text_line_list.append(self.second_list_name)
        current_text_line_list.append(self.first_list_name)
        print(current_text_line_list)
        self.ui_edit_testcase = UIeditTestcase.edit_Testcase([])
        self.ui_edit_testcase.line_list = current_text_line_list
        self.ui_edit_testcase.initUI(self.ui_edit_testcase.line_list)
        self.ui_edit_testcase.show()


    def export_usecase_method(self):
        print("daochu")

    def add_new_testcase(self):
        print("add_new_testcase")
        temp_line_list = []
        try:
            currentItem_text = self.tree.currentItem().text(0)
            print("add_new_testcase--ss:", currentItem_text)
            if not currentItem_text == "所有用例":
                temp_line_list = self.get_line_of_father_item(self.tree.currentItem(), [])
        except:
            print("请选择子目录！")
        if not self.second_list_name == "":
            temp_line_list.append(self.second_list_name)
        temp_line_list.append(self.first_list_name)
        ui_add_testcase.line_list = temp_line_list
        ui_add_testcase.initUI()
        ui_add_testcase.show()
        ui_add_testcase.submit_button.clicked.connect(self.refresh_testcase_tree)

    def refresh_testcase_tree(self):
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        new_path = os.path.join(path, "script", self.first_list_name, self.second_list_name)
        testcases_dict = caf.generate_testcases_to_dict(new_path, {})
        self.tree.clear()
        parent = QTreeWidgetItem(self.tree)
        parent.setText(0, "所有用例")
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        parent.setCheckState(0, Qt.Unchecked)
        self.set_all_testcases(testcases_dict, parent)
        self.tree.show()
        self.tree.clicked.connect(self.print_selected_testcase)
        # self.tree_layout.addWidget(self.tree)
        # self.choice_result_layout.addWidget(self.show_choice_label)

    def get_all_small_types(self, text):
        # 添加二级菜单
        self.first_list_name = text
        self.second_list_name = ""
        self.small_types_combo.clear()
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        new_path = os.path.join(path, "script", text)
        small_types_combo_list = caf.check_all_files(new_path)[0]
        #add_icon = QIcon("ImageDoc/add.jpg")
        self.small_types_combo.addItem("+ add new")
        for c in small_types_combo_list:
            self.small_types_combo.addItem(c)
        self.small_types_combo.activated[str].connect(self.get_all_testcases_by_tag)

    def get_all_testcases_by_tag(self, text):
        # 得到所有测试用例（用例树）
        self.second_list_name = text
        print("get_all_testcases_by_tag", "1", self.first_list_name, "2", self.second_list_name)
        if not self.second_list_name == "+ add new":
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            new_path = os.path.join(path, "script", self.first_list_name, text)
            testcases_dict = caf.generate_testcases_to_dict(new_path, {})
            self.tree.clear()
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, "所有用例")
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            parent.setCheckState(0, Qt.Unchecked)
            self.set_all_testcases(testcases_dict, parent)
            self.tree.show()
            self.tree.clicked.connect(self.print_selected_testcase)
            self.tree_layout.addWidget(self.tree)
            self.choice_result_layout.addWidget(self.show_choice_label)
        else:
            ui_add_small_type.test_group = self.first_list_name
            ui_add_small_type.initUI()
            ui_add_small_type.show()
            ui_add_small_type.submit_button.clicked.connect(self.refresh_small_types_combo)

    def refresh_small_types_combo(self):
        # 刷新二级菜单
        self.small_types_combo.clear()
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        new_path = os.path.join(path, "script", self.first_list_name)
        small_types_combo_list = caf.check_all_files(new_path)[0]
        # add_icon = QIcon("ImageDoc/add.jpg")
        self.small_types_combo.addItem("+ add new")
        for c in small_types_combo_list:
            self.small_types_combo.addItem(c)
        self.small_types_combo.activated[str].connect(self.get_all_testcases_by_tag)

    def get_all_testcases(self, text):
        # 得到所有测试用例（用例树）
        self.first_list_name = text
        self.second_list_name = ""
        print("get_all_testcases", self.first_list_name, self.second_list_name)
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        new_path = os.path.join(path, "script", self.first_list_name)
        testcases_dict = caf.generate_testcases_to_dict(new_path, {})
        self.tree.clear()
        parent = QTreeWidgetItem(self.tree)
        parent.setText(0, "所有用例")
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        parent.setCheckState(0, Qt.Unchecked)
        self.set_all_testcases(testcases_dict, parent)
        self.tree.show()
        self.tree.clicked.connect(self.print_selected_testcase)
        self.tree_layout.addWidget(self.tree)
        self.choice_result_layout.addWidget(self.show_choice_label)

    def print_selected_testcase(self):
        # 打印选中的节点
        test_case_item = QTreeWidgetItemIterator(self.tree)
        test_case_item_list = []
        test_case_item_object_list = []
        while test_case_item.value():
            if test_case_item.value().checkState(0) == Qt.Checked:
                if str(test_case_item.value().text(0)).endswith(".py"):
                    test_case_item_list.append(test_case_item.value().text(0))
                    test_case_item_object_list.append(test_case_item.value())
                else:
                    test_case_item_list.append(test_case_item.value().text(0))

            test_case_item = test_case_item.__iadd__(1)
        new_choice_label_text = ""
        self.total_line_list = []
        for test_case_item_object in test_case_item_object_list:
            self.line_list = self.get_all_line_of_item(test_case_item_object, [])
            if not self.second_list_name == "":
                self.line_list.append(self.second_list_name)
            self.line_list.append(self.first_list_name)
            self.total_line_list.append(self.line_list)

        for tl in test_case_item_list:
            new_choice_label_text = new_choice_label_text + tl + "\n"
        self.show_choice_label.setText(new_choice_label_text)
        self.show_choice_label.show()

        print("total_line_list", self.total_line_list)

    def get_all_line_of_item(self, item, line_list):
        # 得到所有元素的路径
        parent_text = item.parent().text(0)
        line_list.append(item.text(0))
        if not parent_text == "所有用例":
            return self.get_all_line_of_item(item.parent(), line_list)
        else:
            #line_list.append(parent_text)
            return line_list

    def get_line_of_father_item(self, item, line_list):
        # 得到父元素的路径
        parent_text = item.parent().text(0)
        line_list.append(item.text(0))
        if not parent_text == "所有用例":
            return self.get_all_line_of_item(item.parent(), line_list)
        else:
            #line_list.append(parent_text)
            return line_list


    def set_all_testcases(self, testcases_dict, parent):
        # 整合用例树
        if isinstance(testcases_dict, dict):
            for d in testcases_dict.keys():
                if d == "#other":
                    for l in testcases_dict[d]:
                        child = QTreeWidgetItem(parent)
                        child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                        child.setText(0, l)
                        child.setCheckState(0, Qt.Unchecked)
                else:
                    next_parent = QTreeWidgetItem(parent)
                    next_parent.setText(0, d)
                    next_parent.setFlags(next_parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

                    self.set_all_testcases(testcases_dict[d], next_parent)
        elif isinstance(testcases_dict, list):
            for l in testcases_dict:
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, l)
                child.setCheckState(0, Qt.Unchecked)

    def __del__(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def run_test_case(self):
        rti.run_temp_interface(self.total_line_list)
        start()

    def normal_output_written(self, text):
        cursor = self.terminal_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.terminal_text.setTextCursor(cursor)
        self.terminal_text.ensureCursorVisible()

    def close_window(self):
        self.close()


if __name__=="__main__":
#testcase_list = ["a", "b", "c"]
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    new_path = os.path.join(path, "script")
    testcase_list = caf.check_all_files(new_path)[0]
    app = QApplication(sys.argv)
    ex = Choose_testcase(testcase_list)
    # 添加二级菜单添加项
    ui_add_small_type = UIaddSmallType.UIaddSmallType("")
    ui_add_testcase = UIaddTestcase.add_new_testcase_window([])

    sys.exit(app.exec_())
