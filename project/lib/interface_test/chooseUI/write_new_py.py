# -*- coding: UTF-8 -*-

"""
File Name:      write_new_py
Author:         xumohan
Create Date:    2018/7/23
"""
import xlrd
import os

def write_new_py_file(line_list):
    if isinstance(line_list, list):
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        file_name = os.path.join(path, "script")
        for ll in line_list:
            file_name = os.path.join(file_name, ll)
        class_name = line_list[-1][:-3]
    elif isinstance(line_list, str):
        file_name = line_list[:-4] + ".py"
        class_name = line_list.split("\\")[-1][:-4]
    if not os.path.exists(file_name):
        file = open(file_name, 'w')
        file.write("from project.script.testsuite.TestsuiteNormal import *\n")
        file.write("from project.lib.interface_test.testcase import testcase_reader_file_sheet as ts\n")
        file.write("\n\n")
        file.write("class " + class_name + "(TestsuiteNormal):\n")
        file.write("    def setup(self):\n")
        file.write("        pass\n")
        file.write("\n")
        file.write("    def test(self):\n")
        file.write("        file = os.path.join(os.path.dirname(__file__), '" + class_name + ".xml')\n")
        file.write("        ts.run_test_case(file)\n")
        file.write("\n")
        file.write("    def teardown(self):\n")
        file.write("        pass\n")

        file.close()

def change_line_to_new_order(line_list):
    new_line_lists = []
    for l in line_list:
        i = len(l) - 1
        new_line_list = []
        while i>= 0:
            new_line_list.append(l[i])
            i -= 1
        new_line_lists.append(new_line_list)
    return new_line_lists