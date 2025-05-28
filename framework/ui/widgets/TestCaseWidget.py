# -*- coding: UTF-8 -*-

"""
File Name:      TestCaseWidget
Author:         zhangwei04
Create Date:    2018/10/15
"""
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QMouseEvent

from framework.ui.widgets.MenuEdit import MenuEdit
from framework.core.resource import g_resource
from framework.ui.signal.Signal import g_signal
from framework.ui.widgets.AddTestCaseDialog import AddTestCaseDialog


class TestCaseWidget(QTreeWidget):
    """用例与配置栏-用例树组件"""
    def __init__(self):
        super().__init__()
        self.base_dir = os.path.join(g_resource['project_path'], 'script')

        self._create_tree()
        self.setHeaderLabel("用例树")

        self.menu = MenuEdit()
        self._init_menu_UI()
        # 信号连接
        g_signal.get_select_testcase.connect(self.get_selected_testcase)
        g_signal.add_testcase.connect(self.add_testcase_edit)
        g_signal.testcase_tree_reload.connect(self.reload)
        g_signal.project_conf_get_select_testcase.connect(self.get_selected_testcase)

    def _init_menu_UI(self):
        """初始化菜单栏"""
        self.menu.reg_ac("edit_data", "编辑用例数据")
        self.menu.reg_ac("add_to_queue", "添加至运行队列")
        self._menu_trigger_event()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

    def _menu_trigger_event(self):
        """菜单栏组件绑定事件"""
        self.menu.eidt_action.triggered.connect(self.edit_testcase)
        self.menu.add_action.triggered.connect(self.add_testcase)
        self.menu.del_action.triggered.connect(self.delete_testcase)
        self.menu.add_to_queue.triggered.connect(self.add_to_queue)
        self.menu.edit_data.triggered.connect(self.edit_data)

    def show_menu(self):
        """显示菜单栏"""
        try:
            self.menu.show()
            self.menu.exec_(QCursor.pos())
        except Exception as e:
            print(e)

    def edit_testcase(self):
        """编辑用例"""
        try:
            item = self.currentItem()
            item_path = os.path.join(self.base_dir, self._get_path(item))
            dialog_layout = QVBoxLayout()
            # 读取用例文件内容
            self.qte = QTextEdit()
            with open(item_path, 'r', encoding='utf-8') as fp:
                self.qte.setText(fp.read())
            # 保存按钮
            self.qpb = QPushButton("保存用例")
            self.qpb.clicked.connect(self._save_edit)

            dialog_layout.addWidget(self.qte)
            dialog_layout.addWidget(self.qpb)

            qdf = QDialog()
            qdf.setWindowTitle("用例编辑")
            qdf.setLayout(dialog_layout)
            qdf.exec_()
        except Exception as e:
            print(e)

    def _save_edit(self):
        """保存编辑过的用例文件"""
        item = self.currentItem()
        item_path = os.path.join(self.base_dir, self._get_path(item))
        text = self.qte.toPlainText()
        with open(item_path, 'w', encoding='utf-8') as fp:
            fp.write(text)

    def add_testcase(self):
        """添加用例"""
        try:
            dialog_layout = AddTestCaseDialog()
            dialog_layout.exec_()
        except Exception as e:
            print(e)

    @pyqtSlot(str)
    def add_testcase_edit(self, testcace_name):
        """菜单栏添加用例确认后，后台执行添加用例操作
        Args:
            testcace_name: 待添加的用例文件名
        """
        item = self.currentItem()
        item_path = self._get_path(item)
        try:
            item_dir = os.path.split(item_path)[0] if self.is_file(item) else item_path  # item所在目录
            parent = item.parent() if self.is_file(item) else item
        except Exception as e:
            print(e)
        if not testcace_name.endswith(".py"):
            testcace_name += ".py"
        testcase_path = os.path.join(self.base_dir, item_dir, testcace_name)
        with open(testcase_path, 'w', encoding='utf-8') as fp:
            fp.write("# -*- coding: UTF-8 -*-")
        try:
            self._create_node(parent, testcase_path)
        except Exception as e:
            print(e)

    def delete_testcase(self):
        """删除用例"""
        try:
            item = self.currentItem()
            parent = item.parent()
            if parent:
                item_path = self._get_path(item)
                os.remove(os.path.join(self.base_dir, item_path))  # 用例文件删除
                parent.removeChild(item)    # 用例树显示删除
        except Exception as e:
            print(e)

    def add_to_queue(self):
        """添加用例至执行队列"""
        item = self.currentItem()
        print("添加用例至执行队列")

    def edit_data(self):
        """编辑用例数据文件"""
        item = self.currentItem()
        if not self.is_file(item):
            # 目录节点直接返回
            return
        rel_path = self._get_path(item)
        data_path = os.path.join(self.base_dir, rel_path.replace(".py", ".xml"))
        if not os.path.exists(data_path):
            return
        dialog_layout = QVBoxLayout()
        # 读取用例文件内容
        self.qte = QTextEdit()
        with open(data_path, 'r', encoding='utf-8') as fp:
            self.qte.setText(fp.read())
        # 保存按钮
        self.qpb = QPushButton("保存数据")

        self.qpb.clicked.connect(self._save_data_edit)

        dialog_layout.addWidget(self.qte)
        dialog_layout.addWidget(self.qpb)

        qdf = QDialog()
        qdf.setWindowTitle("用例数据编辑")
        qdf.setLayout(dialog_layout)
        self.qpb.clicked.connect(qdf.close)
        qdf.exec_()

    def _save_data_edit(self):
        """保存用例编辑后的用例显示框内容
        """
        item = self.currentItem()
        rel_path = self._get_path(item)
        data_path = os.path.join(self.base_dir, rel_path.replace(".py", ".xml"))
        with open(data_path, "w", encoding='utf-8') as fp:
            fp.write(self.qte.toPlainText())

    def _create_tree(self):
        """创建用例树"""
        self._create_node(self, self.base_dir)

    def _create_node(self, parent, item_dir):
        """递归创建用例节点"""
        if os.path.isdir(item_dir):
            for item in os.listdir(item_dir):
                if item in ("__init__.py","__pycache__") or item.endswith(".xml"):
                    continue
                wid_item = QTreeWidgetItem(parent)
                wid_item.setText(0, item)
                wid_item.setFlags(wid_item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                wid_item.setCheckState(0, Qt.Unchecked)
                if item.endswith(".py"):
                    continue
                self._create_node(wid_item, os.path.join(item_dir, item))
        else:
            if parent is None:
                parent = self
            item = os.path.split(item_dir)[1]
            wid_item = QTreeWidgetItem(parent)
            wid_item.setText(0, item)
            wid_item.setFlags(wid_item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            wid_item.setCheckState(0, Qt.Unchecked)

    @pyqtSlot()
    def get_selected_testcase(self):
        """接受获取勾选的用例信号，从用例树中读取勾选的用例，并返回用例列表
        Returns:
            勾选过的用例列表
        """
        testcase_list = []
        for item in self.get_item():
            # QTreeWidgetItem().checkState()'
            if item.childCount() == 0 and item.checkState(0) != 0:
                testcase_list.append(self._get_path(item))
        g_signal.testcase_tree_selected.emit(testcase_list)
        return testcase_list

    def get_item(self):
        """获取所有节点，生成器方式返回"""
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            yield iterator.value()
            iterator += 1

    # def mouseDoubleClickEvent(self, e, *args, **kwargs):
    #     # print(QApplication.doubleClickInterval())
    #
    #     if e.button() == Qt.RightButton:
    #         try:
    #             print(e.button())
    #             print(self.itemAt(e.pos()).text())
    #             print("mouse double click!!!!!!!")
    #         except Exception as e:
    #             print(e)
    #     try:
    #         self.get_selected_testcase()
    #     except Exception as e:
    #         print(e)

    def is_file(self, item):
        """判断用例节点是否是文件节点"""
        return item.childCount() == 0 and item.text(0).endswith(".py")

    def _get_path(self, item):
        """获取节点的树路径"""
        path = ""
        while True:
            path = "{}/{}".format(item.text(0), path)
            item = item.parent()
            if item is None:
                break
        return path.strip("/")

    def reload(self):
        """重新加载节点"""
        # self._remove_tree()
        # self._create_tree()
        try:
            self.update()
        except Exception as e:
            print(e)

    def _remove_tree(self):
        """删除树"""
        for item in self.get_item():
            try:
                self.removeItemWidget(item, 0)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    testcase_wid = TestCaseWidget()
    testcase_wid.show()
    button = QPushButton()
    button.clicked.connect(testcase_wid.get_selected_testcase)
    button.show()
    sys.exit(app.exec_())