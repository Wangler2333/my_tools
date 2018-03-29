# -*- coding: UTF-8 -*-


import mysql.connector

IP = '127.0.0.1'
USER = 'root'
PASSWD = '88670211'
DATEBASE = 'bookstore'

NewTable = "student"


def connect_mysql():
    ''' 连接数据库 '''
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


def create_table():
    ''' 创建表 '''
    cnn = connect_mysql()
    sql_create_table = 'CREATE TABLE `%s` (`id` int(10) NOT NULL AUTO_INCREMENT,`name`' \
                       ' varchar(10) DEFAULT NULL,`age` int(3) DEFAULT NULL,PRIMARY ' \
                       'KEY (`id`))ENGINE=MyISAM DEFAULT CHARSET=utf8' % NewTable
    cursor = cnn.cursor()
    try:
        cursor.execute(sql_create_table)
    except mysql.connector.Error as e:
        print('create table orange fails!{}'.format(e))


def insert_date():
    ''' 插入数据 '''
    cnn = connect_mysql()
    cursor = cnn.cursor()
    try:
        # 第一种：直接字符串插入方式
        sql_insert1 = "insert into student (name, age) values ('orange', 20)"
        cursor.execute(sql_insert1)

        # 第二种：元组连接插入方式
        sql_insert2 = "insert into student (name, age) values (%s, %s)"

        # 此处的%s为占位符，而不是格式化字符串，所以age用%s
        data = ('shiki', 25)
        cursor.execute(sql_insert2, data)

        # 第三种：字典连接插入方式
        sql_insert3 = "insert into student (name, age) values (%(name)s, %(age)s)"
        data = {'name': 'mumu', 'age': 30}
        cursor.execute(sql_insert3, data)

        # 如果数据库引擎为Innodb，执行完成后需执行cnn.commit()进行事务提交
    except mysql.connector.Error as e:
        print('insert datas error!{}'.format(e))
    finally:
        cursor.close()
        cnn.close()

def search_date():
    ''' 查询操作 '''
    cnn = connect_mysql()
    cursor = cnn.cursor()
    try:
        sql_query = 'select id,name from student where  age > %s'
        cursor.execute(sql_query, (21,))
        for id, name in cursor:
            print ('%s\'s age is older than 25,and her/his id is %d' % (name, id))
    except mysql.connector.Error as e:
        print('query error!{}'.format(e))
    finally:
        cursor.close()
        cnn.close()

def delete_date():
    ''' 删除操作 '''
    cnn = connect_mysql()
    cursor = cnn.cursor()
    try:
        sql_delete = 'delete from student where name = %(name)s and age < %(age)s'
        data = {'name': 'orange', 'age': 24}
        cursor.execute(sql_delete, data)
    except mysql.connector.Error as e:
        print('delete error!{}'.format(e))
    finally:
        cursor.close()
        cnn.close()


if __name__ == '__main__':
    #create_table()
    delete_date()
