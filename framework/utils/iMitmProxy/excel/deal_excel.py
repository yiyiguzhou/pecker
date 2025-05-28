# -*- coding: UTF-8 -*-

"""
File Name:      deal_excel
Author:         zhangwei04
Create Date:    2018/8/3
"""
import re
import os
# from framework.utils.openpyxl import load_workbook
from framework.utils.openpyxl.cell import Cell
from xml.etree.ElementTree import ElementTree as ET
import xml.dom.minidom


class PingBackExcel2Xml(object):
    def __init__(self, file_path, xml_path="tmp.xml"):
        if not os.path.exists(file_path):
            raise FileNotFoundError("{}".format(file_path))
        self._file_path = file_path
        self._xml_path = xml_path
        self._merged_cell_dict = None
        self._row_data_list = []

    def read_excel(self):
        from framework.utils.openpyxl import load_workbook

        wb = load_workbook(filename=self._file_path)
        # wb.active = 1
        sheet = wb.active

        self._merged_cell_dict = self._get_merged(sheet.merged_cells.ranges)

        title_dict = self._get_column_title(sheet, 1)
        self._get_rows_data(sheet, title_dict)

    def write_xml(self):
        if not self._row_data_list:
            self.read_excel()
        doc = xml.dom.minidom.Document()
        root = doc.createElement('data')
        doc.appendChild(root)
        for row_data in self._row_data_list:
            pingback = doc.createElement('pingback')
            for key in row_data:
                date_ele = doc.createElement(key)

                if isinstance(row_data[key], dict):
                    for p_data in row_data[key]:
                        p_data_ele = doc.createElement(p_data)
                        if isinstance(row_data[key][p_data], list):
                            p_data_ele.appendChild(doc.createTextNode(",".join(row_data[key][p_data])))

                        date_ele.appendChild(p_data_ele)
                elif isinstance(row_data[key], type(None)):
                    date_ele.appendChild(doc.createTextNode(""))
                else:
                    date_ele.appendChild(doc.createTextNode(row_data[key]))
                pingback.appendChild(date_ele)

            root.appendChild(pingback)
        with open(self._xml_path, 'w', encoding='utf-8') as fp:
            doc.writexml(fp,indent='\t', addindent='\t', newl='\n', encoding="utf-8")

    def _get_rows_data(self, sheet, title_dict):
        for row_num in range(2, sheet.max_row + 1):
            row_dict = {'desc': "", 'filter': {}, 'common': {}, 'action': {}, 'expect': {}}

            if '用例描述' in title_dict:
                pos_str = self.__get_pos_str_from_merged(row_num, title_dict['用例描述'])
                row_dict['desc'] = sheet[pos_str].value
            if '过滤字段' in title_dict:
                pos_str = self.__get_pos_str_from_merged(row_num, title_dict['过滤字段'])
                self.__str_to_data(sheet[pos_str], row_dict['filter'])
            if '行为action' in title_dict:    # 行为放置过滤字段里面
                pos_str = self.__get_pos_str_from_merged(row_num, title_dict['行为action'])
                self.__str_to_data(sheet[pos_str], row_dict['action'])
            if '通用必投字段' in title_dict:
                pos_str = self.__get_pos_str_from_merged(row_num, title_dict['通用必投字段'])
                self.__str_to_data(sheet[pos_str], row_dict['common'])

            if '全部匹配' in title_dict:
                pos_str = self.__get_pos_str_from_merged(row_num, title_dict['全部匹配'])
                row_dict['is_all_cmp'] = sheet[pos_str].value

            # 其他字段，加到期望值字典中去
            for column_num in range(title_dict['行为action']+1, len(title_dict) + 1):
                if column_num in (title_dict.get('测试结果', None), title_dict.get('备注', None), title_dict.get('测试人员', None)):
                    continue
                pos_str = self.__get_pos_str_from_merged(row_num, column_num)
                self.__str_to_data(sheet[pos_str], row_dict['expect'])

            self._row_data_list.append(row_dict)

    def __get_pos_str_from_merged(self, row_num, column_num):
        column_name = chr(64+column_num)
        pos_str = "%s%d" % (column_name, row_num)
        if pos_str in self._merged_cell_dict:
            pos_str = self._merged_cell_dict[pos_str]

        return pos_str


    def __str_to_data(self, obj_str, obj_dict):
        if isinstance(obj_str, Cell):
            obj_str = obj_str.value
            if obj_str is None:
                return

        for data_str in obj_str.split('\n'):
            data_str = data_str.strip()
            if data_str.startswith('#') or not data_str:
                continue

            if data_str.endswith(('）', ')')):
                index = data_str.rfind('（')
                if index == -1:
                    index = data_str.rfind('(')
                if index == -1:
                    raise Exception("%s 括号不匹配" % data_str)
                data_str = data_str[:index]
            if "=" in data_str:
                data_str_list = data_str.split('=')
                key_str = data_str_list[0]
                value_str = data_str_list[1]
                if '、' in value_str:
                    value_list = value_str.split('、')
                elif ',' in value_str:
                    value_list = value_str.split(',')
                else:
                    value_list = [value_str]
            elif data_str.endswith("not empty"):
                value_list = ['*']
                key_str = data_str.split()[0]
            else: # 只设置了参数名
                value_list = ['*']
                key_str = data_str
            obj_dict[key_str] = value_list

    def _get_column_title(self, sheet, row):
            title_dict = {}
            max_column = sheet.max_column
            max_row = sheet.max_row
            if max_row == row:
                raise Exception("this excel is empty")
            for column_num in range(1, max_column + 1):
                cell = sheet.cell(row=row, column=column_num)
                if not cell.value or not cell.value.strip():
                    raise Exception("标题列长度小于实际列长度，请补充标题")

                if cell.value not in title_dict:    # 标题重名取第一个标题
                    title_dict[cell.value] = column_num
            return title_dict

    def format_merged(self, merged_cell_ranges, pos_string=None, row=None, column=None):
        if pos_string:
            column,row = tuple(pos_string)
        for merged_cell in merged_cell_ranges:
            a = str(merged_cell)

    def _get_merged(self, merged_cell_ranges):
        merged_cell_dict = {}
        for merged_cell in merged_cell_ranges:
            start_column, start_row, end_column, end_row = self._cell_ranges_to_pos(str(merged_cell))
            values = start_column + start_row
            for row in range(int(start_row), int(end_row) + 1):
                if start_column != end_column:
                    for column_ord in range(ord(start_column), ord(end_column) + 1):
                        merged_cell_dict["%s%s" % (chr(column_ord), row)] = values
                else:
                    merged_cell_dict["%s%s" % (start_column, row)] = values
        return merged_cell_dict

    def _cell_ranges_to_pos(self, merged_cell_str):
        cell_list = merged_cell_str.split(":")
        pattern = r'(\D+)(\d+)'
        start_pos = re.findall(pattern, cell_list[0])
        end_pos = re.findall(pattern, cell_list[1])
        return start_pos[0][0], start_pos[0][1], end_pos[0][0], end_pos[0][1]


if __name__ == "__main__":
    px = PingBackExcel2Xml(file_path='Gphone游戏中心测试用例_V6.7.5_数据投递_热修复投递_537.xlsx')
    px.read_excel()
    px.write_xml()
