#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou


import base64
import commands
import hashlib
import os
import sys

secret_key = 'My First Secret Password'
#default_path = os.path.dirname(sys.argv[0]) + '/secretcode'
default_path = '/var/log/secretcode'

Code_introduce = '''
   code 1 : There fail  with get unit info for create secret key file.
   code 2 : This fail was you input password was wrong.
'''


class endecode(object):
    def __init__(self, secret=secret_key, password='SasenyZhou', symbol=None):
        self.secret = secret
        self.base64_encode()
        self.UUID = self.UUID_Get()
        self.password = password
        self.serialnumber = self.serialNumber()
        self.symbol = str(symbol) + ':'

    def base64_encode(self):
        self.second_secret = base64.encodestring(self.secret)

    def UUID_Get(self):
        try:
            UUID = 'None'
            Hardware = commands.getoutput('system_profiler SPHardwareDataType')
            for i in Hardware.split('\n'):
                if 'UUID' in i:
                    UUID = str(i).split(':')[1].replace(' ', '')
            return UUID
        except:
            pass

    def serialNumber(self):
        try:
            serialNumber = 'None'
            Hardware = commands.getoutput('system_profiler SPHardwareDataType')
            for i in Hardware.split('\n'):
                if 'Serial Number' in i:
                    serialNumber = str(i).split(':')[1].replace(' ', '')
            return serialNumber
        except:
            pass

    def hashEncode(self):
        if self.UUID != 'None':
            string_info = str(self.UUID) + str(self.second_secret) + str(self.password) + str(self.serialnumber)
            third_secret = hashlib.sha512()
            third_secret.update(string_info)
            return third_secret.hexdigest()
        else:
            print 'return code 1'
            os._exit(1)

    def writeSecret(self):
        result_code = self.hashEncode()
        if not os.path.isfile(default_path) or self.readSecretFile() == False:
            passwd = raw_input('Pls input password for use [need root]: ')
            if self.password == passwd:
                try:
                    f = open(default_path, 'a')
                    f.write(str(self.symbol) + str(result_code) + '\n')
                    f.close()
                except:
                    pass
            else:
                print 'return code 2'
                os._exit(1)

    def readSecretFile(self):
        try:
            f = open(default_path, 'r')
            f_obj = f.readlines()
            f.close()
            for i in f_obj:
                if self.symbol in i:
                    readInfo = i.split(self.symbol)[1].replace('\n','')
                    break
            return readInfo
        except:
            return False

    def runCheck(self):
        self.writeSecret()
        expect_code = self.hashEncode()
        current_code = self.readSecretFile()
        if expect_code == current_code:
            return True
        else:
            return False


if __name__ == '__main__':
    pass
