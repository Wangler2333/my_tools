#coding=utf-8
# from redis import *
from MysqlHelper import *
from hashlib import sha1
try:
    # redis1=StrictRedis()
    #redis1.set('t2',123)
    #print redis1.get('t2')

    # pip1=redis1.pipeline()
    # pip1.set('t2','abc')
    # pip1.get('t2')
    # pip1.execute()
    # print redis1.get('t3')
    # redis=RedisHelper()
    # print redis.get('t2')

    uname=raw_input("请输入用户名：")
    upwd=raw_input("请输入密码：")

    s1=sha1()
    s1.update(upwd.encode())
    upwd2=s1.hexdigest()

    redis=RedisHelper()
    upwd3=redis.get(uname)
    if upwd3!=None:
        if upwd2==upwd3:
            print('ok')
        else:
            print('密码错误')
    else:
        mysql=MysqlHelper()
        sql='select upwd from users where uname=%s'
        params=[uname]
        result=mysql.fetchone(sql,params)
        if result==None:
            print('用户名不存在')
        elif result[0]==upwd2:
            print('ok')
            redis.set(uname,upwd2)
        else:
            print('密码错误')

except Exception as e:
    print(e)
