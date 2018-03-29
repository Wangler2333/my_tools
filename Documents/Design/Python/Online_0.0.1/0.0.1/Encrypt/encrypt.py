#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/8下午3:46
# @Author   : Saseny Zhou
# @Site     : 
# @File     : encrypt.py
# @Software : PyCharm


import hashlib
from Path.path import *


def password_encrypt(string, Key="加密秘钥"):
    """密码加密"""
    code = hashlib.sha256()
    code.update((str(Key.join(str(string)))).encode("utf-8"))
    return code.hexdigest()


def password_verify(userName, passWord):
    """密码验证"""
    userInfo = read_json_file(userInfoJson)
    if userInfo is not False:
        if userInfo.get(userName, False) is not False:
            if userInfo[userName] == password_encrypt(passWord):
                return True
    return False


def create_userInfo(userName, passWord):
    """新增用户信息"""
    if not os.path.isfile(userInfoJson):
        userInfo = {}
    else:
        userInfo = read_json_file(userInfoJson)
    userInfo[userName] = password_encrypt(passWord)
    write_json_file(userInfo, userInfoJson)

# create_userInfo("root", "not_root")

# print(password_encrypt("123456"))
