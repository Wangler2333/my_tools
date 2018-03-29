#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/23下午4:41
# @Author   : Saseny Zhou
# @Site     : 
# @File     : databases.py
# @Software : PyCharm Community Edition

import sqlite3


class DataBase(object):
    def __init__(self, name):
        self.name = name
        self.conn = sqlite3.connect(self.name)
        self.cur = self.conn.cursor()

    def table_create(self, name):
        try:
            self.cur.execute(
                "create table %s (DATE date, serial_number text, station text, error_code text, Retest text, "
                "unit_number integer,DTI text, Fixture integer, code integer)" % name)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            # print 'sqlite3.OperationalError ', e
            pass

    def insert(self, name, arg):
        self.cur.executemany("insert into %s values (?,?,?,?,?,?,?,?,?)" % name, arg)
        self.conn.commit()

    def update(self, arg):
        self.cur.execute("update stocks set shares=? where symbol=?", (30, 'IBM'))
        self.conn.commit()

    def delete(self, arg):
        self.cur.execute("delete from stocks where symbol=?", ('AIG',))
        self.conn.commit()

    def all(self):
        '''
        # # 选择表中所有的列
        # for row in cur.execute("select * from stocks"):
        #     print row
        # # 选择若干列
        # for shares, price in cur.execute("select shares,price from stocks"):
        #     print shares, price
        #
        # # 选择匹配行
        # for row in cur.execute("select * from stocks where symbol=?", ('IBM',)):
        #     print row
        #
        # # 按照顺序选择匹配行
        # for row in cur.execute("select * from stocks order by shares"):
        #     print row
        #
        # # 逆向选择匹配行
        # for row in cur.execute("select * from stocks order by shares desc"):
        #     print row
        '''
        for row in self.cur.execute("select * from stocks"):
            print row


r = DataBase('test.db')
r.table_create('hehe')

# d = '11/20', 'C02VP002JH8X', 'Run-in', 'h264h265_h9/AVE Factory Tests (Exit code: 45)', \
#     'No', '172', 'J132_P1-19-1_FDLoboCobra17E30741d_FDbridgeOSLoboCobra15P630630z_0_421', '', '1267'
# e = [d]
# r.insert('yyy', e)
