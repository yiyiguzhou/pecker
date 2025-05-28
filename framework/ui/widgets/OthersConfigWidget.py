# -*- coding: UTF-8 -*-

"""
File Name:      OthersConfigWidget
Author:         zhangwei04
Create Date:    2018/10/26
"""
import os

from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QCursor

from framework.ui.widgets.MenuEdit import MenuEdit
from framework.core.resource import g_resource
from framework.ui.signal.Signal import g_signal
from framework.ui.widgets.ConfigWidget import ConfigWidget


class OthersConfigWidget(ConfigWidget):
    """其他配置文件组件，包含邮件配置、用例元素配置文件等"""
    def __init__(self, path, header_lable=""):
        super().__init__(path, header_lable)
        self.base_dir = path

        self.menu = MenuEdit()
        self._init_menu_UI()

    def _init_menu_UI(self):
        """菜单栏初始化"""
        self._menu_trigger_event_bind()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

    def _menu_trigger_event_bind(self):
        """菜单栏绑定事件"""
        self.menu.eidt_action.triggered.connect(self._menu_edit_file)
        # self.menu.add_action.triggered.connect(self._menu_add_file)
        # self.menu.del_action.triggered.connect(self._menu_delete_file)

    def _menu_edit_file(self):
        """菜单栏编辑文件功能"""
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
        qdf.setWindowTitle("配置文件编辑")
        qdf.setLayout(dialog_layout)
        self.qpb.clicked.connect(qdf.close)
        qdf.exec_()

    def _save_conf_data_edit(self):
        """保存文件编辑的内容"""
        item = self.currentItem()
        rel_path = self._get_path(item)
        data_path = os.path.join(self.base_dir, rel_path)
        with open(data_path, "w", encoding='utf-8') as fp:
            fp.write(self.qte.toPlainText())

    def show_menu(self):
        """显示菜单栏"""
        try:
            self.menu.show()
            self.menu.exec_(QCursor.pos())
        except Exception as e:
            print(e)