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
from PyQt5.QtGui import QMouseEvent

from framework.core.resource import g_resource


class ConfigWidget(QTreeWidget):
    """用例与配置栏-配置文件组件"""
    def __init__(self, path, header_lable=""):
        super().__init__()
        self.conf_path = path
        self._load_conf_tree(self, self.conf_path)
        self.setHeaderLabel(header_lable)

    # def mouseDoubleClickEvent(self, e, *args, **kwargs):
    #     print(QApplication.doubleClickInterval())
    #
    #     if e.button() == Qt.RightButton:
    #         try:
    #             print(e.button())
    #             print(self.itemAt(e.pos()).text())
    #             print("mouse double click!!!!!!!")
    #         except Exception as e:
    #             print(e)
    #     self.selected_item()

    def selected_items_text(self):
        """勾选过用例的文本
        Returns:
            文本列表
        """
        return [item.text() for item in self.get_items() if item and item.checkState()]

    def get_items(self):
        """获取配置文件下所有的item"""
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            yield iterator.value()
            iterator += 1

    def _load_conf_tree(self, parent, path):
        """加载配置文件树
        Args:
            parent: 需要挂载的父节点实例
            path: 节点本地路径
        """
        # project_conf_dir = os.path.join(g_resource['project_path'], 'project')
        for conf in os.listdir(path):
            if conf in ('__pycache__',):
                continue
            conf_wid = QTreeWidgetItem(parent)
            conf_wid.setText(0, conf)
            conf_wid.setFlags(conf_wid.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            conf_wid.setCheckState(0, Qt.Unchecked)

            conf_path = os.path.join(path, conf)
            if os.path.isdir(conf_path):
                self._load_conf_tree(conf_wid, conf_path)

    def _get_path(self, item):
        """获取节点树路径
        Args:
            item: 节点实例
        Returns:
            以"/"连接的节点路径
        """
        path = ""
        while True:
            path = "{}/{}".format(item.text(0), path)
            item = item.parent()
            if item is None:
                break
        return path.rstrip("/")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    project_conf_dir = os.path.join(g_resource['project_path'], 'conf')
    conf_wid = ConfigWidget(project_conf_dir)
    conf_wid.show()
    # button = QPushButton()
    # button.clicked.connect(conf_wid.get_selected_testcase)
    # button.show()
    sys.exit(app.exec_())