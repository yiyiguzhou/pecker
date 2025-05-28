# -*- coding: UTF-8 -*-

"""
File Name:      check_all_files 用于UI界面获取下来菜单
Author:         xumohan
Create Date:    2018/7/25
"""
import os


def check_all_files(dir_name):
    dir_list = []
    file_list = []
    if os.path.exists(dir_name):
        dirs = os.listdir(dir_name)
        for d in dirs:
            if not d == '__pycache__':
                d_path = os.path.join(dir_name, d)
                if os.path.isdir(d_path):
                    dir_list.append(d)
                else:
                    file_list.append(d)
    return dir_list, file_list


def whether_it_is_dict(dirs_path):
    if os.path.isdir(dirs_path):
        dirs = os.listdir(dirs_path)
        for dir in dirs:
            if dir != '__pycache__' and dir != '__init__.py':
                if os.path.isdir(os.path.join(dirs_path, dir)):
                    return True
    return False


def generate_testcases_to_dict(dir_name, testcases_dict):
    # 整合用例
    if os.path.isdir(dir_name):
        dirs = os.listdir(dir_name)

        for dir in dirs:
            if dir != '__pycache__' and dir != '__init__.py':
                ss = os.path.join(dir_name, dir)
                if whether_it_is_dict(os.path.join(dir_name, dir)):
                    testcases_dict[dir] = {}

                    generate_testcases_to_dict(os.path.join(dir_name, dir), testcases_dict[dir])
                else:

                    if os.path.isdir(os.path.join(dir_name, dir)):
                        if not dir in testcases_dict.keys():
                            testcases_dict[dir] = []
                        other_list = check_all_files(os.path.join(dir_name, dir))[1]
                        for l in other_list:
                            if l != '__init__.py':
                                if str(l).endswith(".py"):
                                    testcases_dict[dir].append(l)
                    else:
                        if not "#other" in testcases_dict.keys():
                            testcases_dict["#other"] = []
                        if str(dir).endswith(".py"):
                            testcases_dict["#other"].append(dir)
    else:
        if not "#other" in testcases_dict.keys():
            testcases_dict["#other"] = []
        other_list = check_all_files(dir_name)[1]
        for l in other_list:
            if l != '__init__.py':
                if str(l).endswith(".py"):
                    testcases_dict["#other"].append(l)
    return (testcases_dict)




# path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# new_path = os.path.join(path, "script", "interface_test", "houtai")
# #dir_list = check_all_files(new_path)
# #print(dir_list)
# testcases_dict = generate_testcases_to_dict(new_path, {})
#
# print(testcases_dict)
