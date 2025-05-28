# -*- coding: UTF-8 -*-

"""
File Name:      write_temp_xml
Author:         xumohan
Create Date:    2018/7/23
"""
import os
from xml.dom.minidom import Document


def get_temp_element_tree(line_list):
    doc = Document()
    project = doc.createElement("project")
    project.setAttribute("sort", "normal")
    project.setAttribute("loop", "1")
    for l in line_list:
        testcase = doc.createElement("testcase")
        testcase.setAttribute("loop", "1")
        testcase_text_content = ""

        for ll in l:
            testcase_text_content = testcase_text_content + str(ll) + "/"
        testcase_text_content = testcase_text_content[:-4]
        testcase_text = doc.createTextNode(testcase_text_content)
        testcase.appendChild(testcase_text)
        project.appendChild(testcase)
    doc.appendChild(project)
    return doc


def write_new_xml(line_list):
    doc_tree = get_temp_element_tree(line_list)
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    new_path = os.path.join(path, "project")
    file_name = os.path.join(new_path, "test_temp_xml.xml")
    if os.path.exists(file_name):
        os.remove(file_name)
    file = open(file_name, 'w', encoding='utf-8')
    file.write(doc_tree.toprettyxml())
    file.close()



