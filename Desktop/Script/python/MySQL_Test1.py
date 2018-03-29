# -*- coding: UTF-8 -*-

import mysql.connector
import os
import csv

IP = '127.0.0.1'
#IP = '172.22.145.137'
USER = 'root'
PASSWD = '88670211'
DATEBASE = 'TEST_ITEM'
NewTable = "NAND_TEST"

path_road = "/Users/saseny/Desktop/NAND.csv"

if not os.path.isfile(path_road):
    print 'File \'' + str(path_road) + '\' was not exists!'
    os._exit(-1)


def connect_mysql_for_database_create():
    config = {
        'host': IP,
        'user': USER,
        'password': PASSWD,
        'port': 3306,
        'charset': 'utf8'
    }
    try:
        cnn = mysql.connector.connect(**config)
        return cnn
    except mysql.connector.Error as a:
        print ('connect fails!{}'.format(a))


def creat_database():
    cnn = connect_mysql_for_database_create()
    sql_create_database = 'CREATE DATABASE IF NOT EXISTS %s' % DATEBASE
    cursor = cnn.cursor()
    try:
        cursor.execute(sql_create_database)
    except mysql.connector.Error as d:
        print('create database orange fails!{}'.format(d))


def delect_datebase():
    cnn = connect_mysql_for_database_create()
    sql_delect_database = 'DROP DATABASE IF EXISTS %s' % DATEBASE
    cursor = cnn.cursor()
    try:
        cursor.execute(sql_delect_database)
    except mysql.connector.Error as d:
        print('delect database orange fails!{}'.format(d))


def writecsv(data, path):
    if not os.path.isfile(path):
        c = ['Test Item', 'Code', 'Test Info', 'Message']
        writer = csv.writer(open(path, 'a'))
        writer.writerow(c)
    writer = csv.writer(open(path, 'a'))
    writer.writerow(data)


def create_table():
    cnn = connect_mysql()
    sql_create_table = 'CREATE TABLE IF NOT EXISTS `%s` (`id` int(10) NOT NULL AUTO_INCREMENT,`Item` TEXT DEFAULT NULL,`Code`' \
                       ' TEXT DEFAULT NULL,`Info` TEXT DEFAULT NULL, `Message` TEXT DEFAULT NULL,PRIMARY ' \
                       'KEY (`id`))ENGINE=MyISAM DEFAULT CHARSET=utf8' % NewTable
    cursor = cnn.cursor()
    try:
        cursor.execute(sql_create_table)
    except mysql.connector.Error as e:
        print('create table orange fails!{}'.format(e))


def readcsv(path):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print row['Test Item'], '\t', row[' Error Code'], '\t', row[' Test Info'], '\t',  row[' Message']
            if search_date(row['Test Item'], row[' Error Code']) == True:
                print '[' + str(row['Test Item']) + ' ' + str(row[' Error Code']) + ']' + "\t 数据已存在."
            elif row[' Error Code']:
                print '[' + str(row['Test Item']) + ' ' + str(row[' Error Code']) + ']' + "\t 不存在，加载中..."
                insert_date(row['Test Item'], row[' Error Code'], row[' Test Info'], row[' Message'])


def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)


def connect_mysql():
    config = {
        'host': IP,
        'user': USER,
        'password': PASSWD,
        'port': 3306,
        'database': DATEBASE,
        'charset': 'utf8'
    }
    try:
        cnn = mysql.connector.connect(**config)
        return cnn
    except mysql.connector.Error as a:
        print ('connect fails!{}'.format(a))


def search_date(item, code):
    cnn = connect_mysql()
    cursor = cnn.cursor()
    try:
        sql_query = 'select Item, Code, Info, Message from NAND_TEST where Item = %s and Code = %s'
        cursor.execute(sql_query, (item, code))
        for a, b, c, d in cursor:
            # print a, b, c, d
            return True
    except mysql.connector.Error as e:
        print('query error!{}'.format(e))
    finally:
        cursor.close()
        cnn.close()


def insert_date(TestItem, ErrorCode, TestInfo, Message):
    cnn = connect_mysql()
    cursor = cnn.cursor()
    try:
        sql_insert2 = "insert into NAND_TEST (Item, Code, Info, Message) values (%s, %s, %s, %s)"
        data = (TestItem, ErrorCode, TestInfo, Message)
        cursor.execute(sql_insert2, data)
        print "\t \t 数据加载成功."
    except mysql.connector.Error as e:
        print "\t \t 数据加载失败，请查看原因."
        print('insert datas error!{}'.format(e))
    finally:
        cursor.close()
        cnn.close()


def delete_date():
    cnn = connect_mysql()
    cursor = cnn.cursor()
    try:
        sql_delete = 'delete from NAND_TEST where Item = %(name)s'
        data = {'name': "Should be for iMac only."}
        cursor.execute(sql_delete, data)
    except mysql.connector.Error as e:
        print('delete error!{}'.format(e))
    finally:
        cursor.close()
        cnn.close()


if __name__ == '__main__':
    #readcsv(path_road)
    creat_database()
    create_table()
    #delect_datebase()
    readcsv(path_road)
    #delete_date()
