# -*- coding: UTF-8 -*-

"""
File Name:      ConfigWidget
Author:         zhangwei04
Create Date:    2018/10/15
"""
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QMouseEvent

from framework.core.resource import g_resource
from framework.ui.signal.Signal import g_signal
from framework.ui.widgets.ConfigWidget import ConfigWidget
from framework.ui.widgets.MenuEdit import MenuEdit


class ProjectConfigWidget(ConfigWidget):
    """用例状态栏-工程配置组件"""
    def __init__(self, path, header_lable=""):
        super().__init__(path, header_lable)
        self.testcase_list = None

        self.base_dir = path

        self.menu = MenuEdit()
        self._init_menu_UI()

        g_signal.testcase_tree_selected.connect(self.selected_testcase)
        g_signal.get_select_xml.connect(self.get_select_xml)
        g_signal.get_select_aml.connect(self.get_select_aml)

    def _init_menu_UI(self):
        """初始化菜单UI界面"""
        self._menu_trigger_event_bind()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

    def _menu_trigger_event_bind(self):
        """菜单事件绑定"""
        self.menu.eidt_action.triggered.connect(self._menu_edit_file)
        self.menu.add_action.triggered.connect(self._menu_add_file)
        self.menu.del_action.triggered.connect(self._menu_delete_file)

    def show_menu(self):
        """显示菜单"""
        try:
            self.menu.show()
            self.menu.exec_(QCursor.pos())
        except Exception as e:
            print(e)

    def _menu_edit_file(self):
        """菜单编辑配置文件功能"""
        item = self.currentItem()
        conf_path = os.path.join(self.base_dir, self._get_path(item))
        if not os.path.isfile(conf_path):
            # 目录节点直接返回
            return
        dialog_layout = QVBoxLayout()
        self.qte = QTextEdit()
        with open(conf_path, 'r', encoding='utf-8') as fp:
            self.qte.setText(fp.read())
        # 保存按钮
        self.qpb = QPushButton("保存数据")

        self.qpb.clicked.connect(self._save_conf_data_edit)

        dialog_layout.addWidget(self.qte)
        dialog_layout.addWidget(self.qpb)

        qdf = QDialog()
        qdf.setWindowTitle("用例数据编辑")
        qdf.setLayout(dialog_layout)
        self.qpb.clicked.connect(qdf.close)
        qdf.exec_()

    def _save_conf_data_edit(self):
        """保存编辑文件内容"""
        item = self.currentItem()
        rel_path = self._get_path(item)
        data_path = os.path.join(self.base_dir, rel_path)
        with open(data_path, "w", encoding='utf-8') as fp:
            fp.write(self.qte.toPlainText())

    def _menu_add_file(self):
        """添加配置文件"""
        print("暂不支持配置文件的添加")
        item = self.currentItem()

    def _menu_delete_file(self):
        """删除配置文件"""
        print("暂不支持配置文件的删除")
        item = self.currentItem()

    def get_select_xml(self):
        """获取勾选的xml文件(用例配置文件)，通过信号方式发送获取的xml列表"""
        xml_list = self.get_checked_file(".xml")
        g_signal.xml_selected.emit(xml_list)

    def get_select_aml(self):
        """获取勾选的aml文件(设备配置文件)，通过信号方式发送获取的aml列表"""
        aml_list = self.get_checked_file(".aml")
        if len(aml_list) == 0:
            reply = QMessageBox.warning(self, "警告", "请选择一个设备配置文件，当前未勾选", QMessageBox.Yes)
            return
        elif len(aml_list) > 1:
            comment = "\n".join(aml_list)
            reply = QMessageBox.warning(self, "警告", "请选择一个设备配置文件，已选\n{}\n文件".format(comment), QMessageBox.Yes)
            return

        g_signal.send_aml_file.emit(aml_list[0])
        # g_signal.aml_selected.emit(aml_list)

    def selected_testcase(self, testcase_list):
        """勾选的用例槽"""
        self.testcase_list = testcase_list

    def get_checked_file(self, dot='.aml'):
        """
        获取勾选过的用例
        :param dot: 文件后缀名
        :return:
        """
        file_list = []
        for item in self.get_items():
            if item.checkState(0) != 0:
                node_name = item.text(0)
                if node_name.endswith(dot):
                    file_list.append(self._get_path(item))
        return file_list

    def is_file(self, item):
        """判断节点是否是文件节点，只xml和aml后缀文件"""
        return item.childCount() == 0 and item.text(0).endswith((".xml", ".aml"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    conf_wid = ProjectConfigWidget()
    conf_wid.show()
    # button = QPushButton()
    # button.clicked.connect(conf_wid.get_selected_testcase)
    # button.show()
    sys.exit(app.exec_())