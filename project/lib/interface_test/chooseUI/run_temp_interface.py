# -*- coding: UTF-8 -*-

"""
File Name:      run_temp_interface
Author:         xumohan
Create Date:    2018/7/23
"""
import os
from project.lib.interface_test.chooseUI import write_new_py, write_temp_xml

def run_temp_interface(line_list):
    line_list = write_new_py.change_line_to_new_order(line_list)
    for l in line_list:
        write_new_py.write_new_py_file(l)
    write_temp_xml.write_new_xml(line_list)

def run_edit_interface(file_path):
    paths = os.path.split(file_path)




# line_list = [["UGameList_listByGameOnlineDate.py", "testUI", "interface_test"], ["UGameList_list.py", "testUI", "interface_test"]]
# run_temp_interface(line_list)
