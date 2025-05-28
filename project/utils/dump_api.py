# -*- coding: UTF-8 -*-

"""
File Name:      dump_api
Author:         zhangwei04
Create Date:    2019/4/25
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
def dump_api():
    cur_dir = os.path.dirname(__file__)
    os.chdir(os.path.join(cur_dir, "..", "lib", "gamecenter"))

def get_api_modules():
    module_list = []
    api_file_dir = os.path.join(os.path.dirname(__file__), "..",  )