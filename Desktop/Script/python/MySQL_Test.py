# -*- coding: UTF-8 -*-

import mysql.connector
import sys, os
import csv

IP = '127.0.0.1'
USER = 'root'
PASSWD = '88670211'
DATEBASE = 'IDENTITY_CARD'
NewTable = "CARD_ID"

path_road = "/Users/sasenyzhou/Desktop/ID.csv"


def writecsv(data, path):
    if not os.path.isfile(path):
        c = ['关系', '姓名', '身份证号码']
        writer = csv.writer(open(path, 'a'))
        writer.writerow(c)
    writer = csv.writer(open(path, 'a'))
    writer.writerow(data)


def create_table():
    cnn = connect_mysql()
    sql_create_table = 'CREATE TABLE IF NOT EXISTS `%s` (`编号` int(10) NOT NULL AUTO_INCREMENT,`关系` varchar(20) DEFAULT NULL,`姓名`' \
                       ' varchar(10) DEFAULT NULL,`身份证号码` varchar(20) DEFAULT NULL,PRIMARY ' \
                       'KEY (`编号`))ENGINE=MyISAM DEFAULT CHARSET=utf8' % NewTable
    cursor = cnn.cursor()
    try:
        cursor.execute(sql_create_table)
    except mysql.connector.Error as e:
        print('create table orange fails!{}'.format(e))


def readcsv(path):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print row['关系'], '\t', row['姓名'], '\t', row['身份证号码']
            if search_date(row['姓名']) == True:
                print '[' + str(row['姓名']) + ']' + "\t 数据已存在."
            else:
                print '[' + str(row['姓名']) + ']' + "\t 不存在，加载中..."
                insert_date(row['关系'], row['姓名'], row['身份证号码'])


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


def search_date(id):
    cnn = connect_mysql()
    cursor = cnn.cursor()
    try:
        sql_query = 'select * from CARD_ID where 姓名 = %s'
        cursor.execute(sql_query, (id,))
        for a, b, c, d in cursor:
            # print a, b, c, d
            return True

    except mysql.connector.Error as e:
        print('query error!{}'.format(e))
        return False
    finally:
        cursor.close()
        cnn.close()


def insert_date(drmt, name, id):
    cnn = connect_mysql()
    cursor = cnn.cursor()
    try:
        sql_insert2 = "insert into CARD_ID (关系, 姓名, 身份证号码) values (%s, %s, %s)"
        data = (drmt, name, id)
        cursor.execute(sql_insert2, data)
        print "\t \t 数据加载成功."
    except mysql.connector.Error as e:
        print "\t \t 数据加载失败，请查找原因."
        print('insert datas error!{}'.format(e))
    finally:
        cursor.close()
        cnn.close()


def delete_date(name):
    cnn = connect_mysql()
    cursor = cnn.cursor()
    try:
        sql_delete = 'delete from CARD_ID where 姓名 = %(name)s'
        data = {'name': name}
        cursor.execute(sql_delete, data)
    except mysql.connector.Error as e:
        print('delete error!{}'.format(e))
    finally:
        cursor.close()
        cnn.close()


if __name__ == '__main__':
    create_table()
    readcsv(path_road)
    d = ['女父','陈俊兵','321025196703104018']
    writecsv(d,path_road)
    #delete_date('陈蓉')

