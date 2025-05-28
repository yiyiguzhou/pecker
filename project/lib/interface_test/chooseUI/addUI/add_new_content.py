# -*- coding: UTF-8 -*-

"""
File Name:      add_new_content
Author:         xumohan
Create Date:    2018/7/30
"""
import os


def add_new_type(first_drop_box, second_drop_box_name):
    base_file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    new_doc_name = os.path.join(base_file_path, "script", first_drop_box, second_drop_box_name)
    os.makedirs(new_doc_name)


# first_drop_box = "interface_test"
# second_drop_box_name = "test_add"
# add_new_type(first_drop_box, second_drop_box_name)



