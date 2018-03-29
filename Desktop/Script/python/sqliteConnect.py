import sqlite3

'''
SQLite 数据库操作模块
数据库建立
表单建立   : mydata , ip_list
数据插入   : mydate   -> ID, IPADDRESS, PRODUCT, LINEID, STATION, GH_NAME, BOBCAT, DISK, TIME, OVERLAY
                        "1", "172.23.171.196", "J79A", "F6-1FT-C16", "2", "J79A POST-PI-ROUTER", "OFF", "12%",
                        "2017-09-05 12:12:12", "20170828_185514_j79a post-pi-router_1.4.13Fatp"
            ip_list  -> ID, IPADDRESS
数据搜索
数据更新
数据删除
'''


class DataBase(object):
    def __init__(self, databasename="test.db", insertDict=None):
        self.database = databasename
        self.cnn = sqlite3.connect(self.database)
        self.insertData = insertDict

    def createContentTable(self):
        create_table = 'CREATE TABLE mydata (ID INTEGER PRIMARY KEY NOT NULL, IPADDRESS VARCHAR(20),PRODUCT VARCHAR(20),LINEID VARCHAR(20),STATION VARCHAR(5),' \
                       'GH_NAME VARCHAR(30),BOBCAT VARCHAR(5),DISK VARCHAR(20),TIME VARCHAR(30),OVERLAY VARCHAR(100))'
        cur = self.cnn.cursor()
        try:
            cur.execute(create_table)
        except sqlite3.Error as e:
            print('create table orange fails! {}'.format(e))

    def createIPTable(self):
        create_table = 'CREATE TABLE ip_list (ID INTEGER PRIMARY KEY NOT NULL, IPADDRESS TEXT)'
        cur = self.cnn.cursor()
        try:
            cur.execute(create_table)
        except sqlite3.Error as e:
            print('create table orange fails! {}'.format(e))

    def insertContent(self, data):
        self.cnn.commit()
        cur = self.cnn.cursor()
        try:
            sql_insert = "insert into mydata (ID, IPADDRESS, PRODUCT, LINEID, STATION, GH_NAME, BOBCAT, DISK, TIME, OVERLAY) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cur.execute(sql_insert, data)
            self.cnn.commit()
        except sqlite3.Error as e:
            print('create table orange fails! {}'.format(e))

    def insertIP(self, date=(None, None)):
        insret = True
        iplist = self.searchIP()
        for i in iplist:
            if i[1] == date[1]:
                insret = False
        if insret == True:
            self.cnn.commit()
            cur = self.cnn.cursor()
            try:
                sql_insert = "insert into ip_list (ID, IPADDRESS) values (?, ?)"
                cur.execute(sql_insert, date)
                self.cnn.commit()
            except sqlite3.Error as e:
                print('create table orange fails! {}'.format(e))

    def searchContent(self, id):
        self.cnn.commit()
        cur = self.cnn.cursor()
        sql_cmd = "select * from mydata where ID=%s" % id
        try:
            cur.execute(sql_cmd)
        except sqlite3.Error as e:
            print('create table orange fails! {}'.format(e))
        return cur.fetchall()

    def searchIP(self):
        self.cnn.commit()
        cur = self.cnn.cursor()
        try:
            cur.execute("select * from ip_list")
        except sqlite3.Error as e:
            print('create table orange fails! {}'.format(e))
        return cur.fetchall()

    def updateContent(self):
        self.cnn.commit()
        cur = self.cnn.cursor()
        sql_cmd = "update ip_list set IPADRESS=%s where ID=%s" % ("123", "3")
        try:
            cur.execute(sql_cmd)
            self.cnn.commit()
        except sqlite3.Error as e:
            print('create table orange fails! {}'.format(e))

    def deleteIP(self, id):
        self.cnn.commit()
        cur = self.cnn.cursor()
        sql_cmd = "delete from ip_list where id = %s" % id
        try:
            cur.execute(sql_cmd)
            self.cnn.commit()
        except sqlite3.Error as e:
            print('create table orange fails! {}'.format(e))

    def deleteConnect(self, id):
        self.cnn.commit()
        cur = self.cnn.cursor()
        sql_cmd = "delete from mydata where id = %s" % id
        try:
            cur.execute(sql_cmd)
            self.cnn.commit()
        except sqlite3.Error as e:
            print('create table orange fails! {}'.format(e))


if __name__ == '__main__':
    pass
