# -*- coding:utf-8 -*-
import copy

import pymysql
import pymysql.cursors

from project.lib.interface_test.database import DtbaseTable


class Database:
    # 链接数据库
    def get_connect(self, host, database):
        if not host == 'bd.gameplat2qc.w.qiyi.db':
            trcf = DtbaseTable.Config_read()
            port,user, passwd = trcf.getDatabase(host)[0],trcf.getDatabase(host)[1], trcf.getDatabase(host)[2]
        else:
            port = 1517
            user = 'game_qc_user'
            passwd = 'eA8XEZE2WnXp'
        db = pymysql.connect(host=host,
                             db=database,
                             port=port,
                             user=user,
                             passwd=passwd,
                             charset='utf8')
        return db


    # 自用函数，用于添加数据库和表的配置的时候添加所有列名，程序里并不使用
    def show_all_columns(self, host, database, table_name):

        db = self.get_connect(host, database)
        cur = db.cursor()

        try:
            sql = 'DESCRIBE ' + table_name
            cur.execute(sql)
            # 使用 fetchone() 方法获取一条数据库。
            rows = cur.fetchall()

            datalist = []

            for r in rows:
                r = list(r)[0]
                datalist.append(str(r))
            print (datalist)
        finally:
            # 关闭数据库连接
            cur.close()
            db.close()

    # 查看字段在不在数据库里（这个函数重了）
    # parameter: table_name:表名字(table名字里要包含), ekey:传入字段
    def check_key_in_database(self, host, database, table_name, ekey):

        db = self.get_connect(host, database)
        cur = db.cursor()

        try:
            sql = 'DESCRIBE ' + table_name
            cur.execute(sql)
            # 使用 fetchone() 方法获取一条数据库。
            rows = cur.fetchall()
            rowlist = list(rows)
            datalist = []

            for r in rows:
                r = list(r)[0]
                datalist.append(r)
            print (datalist)
            if ekey in datalist:
                return 'you'
            else:
                return 'meiyou'

        finally:
            # 关闭数据库连接
            cur.close()
            db.close()

    # 根据一个key找到数据库里的结果
    def select_one_key(self, host, database, database_keyword, database_name, condition):
        db = self.get_connect(host, database)
        cur = db.cursor()

        try:
            sql = 'SELECT ' + database_keyword + ' from ' + database_name

            if condition != '':
                sql = sql +" WHERE "+ condition
            cur.execute(sql)
            # 使用 fetchone() 方法获取一条数据库。
            rows = cur.fetchall()
            rowlist = list(rows)
            dataset = set([])

            for r in rowlist:
                r = list(r)[0]
                dataset.add(r)
            return dataset


        finally:
            # 关闭数据库连接
            cur.close()
            db.close()

    # 特殊查询
    def special_select(self, host, database, SQL, condition, database_page_size, filename):

        db = self.get_connect(host, database)
        cur = db.cursor()

        try:
            sql = SQL

            if condition != '':
                if 'LIMIT' in sql:
                    sql, sql_limit = sql.split("LIMIT")
                else:
                    sql_limit = ""
                if 'WHERE' in sql:
                    sql = sql + ' AND a.' + condition
                else:
                    sql = sql + ' WHERE a.' + condition
                if not sql_limit == "":
                    sql = sql + " LIMIT" +sql_limit
            if database_page_size != '':
                if 'LIMIT' in sql:
                    sql, sql_limit = sql.split("LIMIT")
                sql = sql + ' LIMIT ' + database_page_size + ' ;'

            cur.execute(sql)
            # 使用 fetchone() 方法获取一条数据库。
            rows = cur.fetchall()
            rowlist = list(rows)
            dataset = set([])

            for r in rowlist:
                r = list(r)[0]
                dataset.add(r)
            return dataset


        finally:
            # 关闭数据库连接
            cur.close()
            db.close()

    # 得到特殊查询的列表，用于验证排序
    def get_list(self, sql, host, database):
        db = self.get_connect(host, database)
        cur = db.cursor()

        try:
            cur.execute(sql)
            # 使用 fetchone() 方法获取一条数据库。
            rows = cur.fetchall()
            rowlist = list(rows)
            datalist = []

            for r in rowlist:
                r = list(r)[0]
                datalist.append(r)
            return datalist


        finally:
            # 关闭数据库连接
            cur.close()
            db.close()

    # 得到dict
    def get_dict(self, sql, host, database):
        db = self.get_connect(host, database)
        cur = db.cursor()

        try:
            cur.execute(sql)
            # 使用 fetchone() 方法获取一条数据库。
            rows = cur.fetchall()
            rowlist = list(rows)
            datadict = {}
            datalists = []
            for r in rowlist:
                for i in range(len(cur.description)):
                    datadict[cur.description[i][0]] = int(list(r)[i])
                datadict2 = copy.deepcopy(datadict)
                datalists.append(datadict2)
                #datadict.clear()
            return datalists

        finally:
            # 关闭数据库连接
            cur.close()
            db.close()
