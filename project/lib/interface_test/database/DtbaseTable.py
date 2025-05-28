# coding=utf-8
import configparser
from project.script.testsuite.TestsuiteNormal import *
from project.lib.interface_test.utils import Singleton

class Config_read(object):
    def get_value(self,filename):
        file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.join('\DtbaseTable.ini')
        file_path = os.path.abspath(file_path)

        config = configparser.ConfigParser()
        config.read(file_path)
        #print file_path

        host = config.get(filename, 'host')
        database = config.get(filename, 'database') #分别代表所在区域名 和变量名
        table = config.get(filename, 'table')
        column = config.get(filename, 'column')
        tcolumn = config.get(filename, 'tcolumn')
        special = config.get(filename, 'special')

        return (host, database, table, column, tcolumn, special)

    def get_database(self, hostname):
        file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.join('\DtbaseTable.ini')
        file_path = os.path.abspath(file_path)

        config = configparser.ConfigParser()
        config.read(file_path)
        # print file_path

        port = config.get(hostname, 'port')
        user = config.get(hostname, 'user')
        passwd = config.get(hostname, 'passwd')


        return (port, user, passwd)

    # 查询是不是在数据库字段里
    def checkKey(self, filename, ekey):
        trcf = Config_read()
        columnlist = trcf.get_value(filename)[3].replace('\'','').replace(' ','').split(',')

        if ekey in columnlist:
            return True
        else:
            return False

    # 查询是不是在联表查询字段
    def check_key_in_union(self, filename, ekey):
        trcf = Config_read()
        columnlist = trcf.get_value(filename)[4].replace('\'', '').replace(' ', '').split(',')

        if ekey in columnlist:
            return True
        else:
            return False

    # 判断是不是特殊查询的key
    def check_special(self, filename, ekey):
        trcf = Config_read()
        columnlist = trcf.get_value(filename)[5].replace('\'','').replace(' ','').split(',')
        if ekey in columnlist:
            return True
        else:
            return False

    # 直接获得特殊查询的sql
    def get_special_select(self, key):
        file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.join('\SpecialSelect.ini')
        file_path = os.path.abspath(file_path)

        config = configparser.ConfigParser()
        config.read(file_path)
        # print file_path

        host = config.get(key, 'host')
        sql = config.get(key, 'sql')  # 分别代表所在区域名 和变量名
        return host, sql

    # 把SpecialSQL里的内容整合成SQL
    def generate_sql(self,  file, key, parameter, flag):
        file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.join('\SpecialSQL.ini')
        file_path = os.path.abspath(file_path)

        config = configparser.ConfigParser()
        config.read(file_path)
        # print file_path

        select = config.get(file, 'select')
        fromc = config.get(file, 'from')
        where = config.get(file, 'where')
        group = config.get(file, 'group')
        order = config.get(file, 'order')
        limit = config.get(file, 'Limit')

        place = self.get_sql_place(key, file)

        if place == "select":
            select = select + key
        if select == "":
            select = "a.game_id"
        sql = "SELECT " + select + " FROM " + fromc
        kvs = parameter.split("&")
        pdict = {}
        for kv in kvs:
            k, v = kv.split("=")
            pdict[k] = v
        if key in pdict.keys():
            kvalue = pdict[key]
        if place == "where":
            where = where

            if "," in kvalue:
                if where !='':
                    sql = sql + " WHERE " + where + " AND " + key + " in (" + kvalue + ")"
                else:
                    sql = sql + " WHERE " + key + " in (" + kvalue + ")"
            else:
                if where !='':
                    sql = sql + " WHERE " + where + " AND " + key + "=" + kvalue
                else:
                    sql = sql + " WHERE " + key + "=" + kvalue
        elif where != "":
            sql = sql + " WHERE " + where

        if group !='':
            sql = sql + " GROUP BY " + group

        if file == "MGameList_gameList" and flag == "checkSort":
            kvs = parameter.split("&")
            pdict = {}
            for kv in kvs:
                k, v = kv.split("=")
                pdict[k] = v

            sort = pdict["sort"]
            sql = sql + " ORDER BY " + key + " " + sort

        elif place == "order":
                sql = sql + " ORDER BY " + key
                if "sort" in pdict.keys():
                    sql = sql + " " + pdict["sort"]
                else:
                    sql = sql + " " + "desc"
        elif order !='':
            sql = sql + " ORDER BY " + order
            if "sort" in pdict.keys():
                sql = sql + " " + pdict["sort"]
            else:
                sql = sql + " " + "desc"


        if place == "limit":

            if "page" in pdict.keys():
                page = int(pdict["page"])
                pvalue = (page-1)*10
            else:
                pvalue = 0
            if "page_size" in pdict.keys():
                psvalue = pdict["page_size"]
            elif "per_page" in pdict.keys():
                psvalue = pdict["per_page"]
            elif "limit" in pdict.keys():
                psvalue = pdict["limit"]
            else:
                psvalue = 20
            limit = str(pvalue) + "," + str(psvalue)
            sql = sql + " LIMIT " + limit

        elif limit !='':
            sql = sql + " LIMIT " + limit
        #print("sql: ", sql)
        return sql


    def check_places_in_pr_not(self, SQLplaces, key):
        for k in SQLplaces.keys():
            if key in SQLplaces[k]:
                place = k
                a_result = True
                break
            else:
                a_result = False
        return a_result


    def get_sql_place(self, key, filename):

        SQLplaces = {
            "select":["need_auth","online_date","isshield_gamecenter","pay_status","","","","","","","",""],
            "where":["network","publish_area","online_status","terminal"],
            "limit":["page","limit","per_page","","",""],
            "order":[]
        }

        if filename == "MGameList_gameList" and key == "online_date":
            place = "order"
            a_result = True
        else:
            for k in SQLplaces.keys():
                if key in SQLplaces[k]:
                    place = k
                    break
        obj = Singleton.Singleton.get_instance("11", "22", False)
        expect_true(self.check_places_in_pr_not(SQLplaces, key), obj.id + " 添加新的SQL的字段位置")
        return place


