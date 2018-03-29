#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __author__: Saseny Zhou

import os, sys
import commands

source_file = ['/Volumes/MaxDisk/Phoenix/Logs', '/Volumes/LoboMini/Phoenix/Logs','/Volumes/MaxDisk/Phoenix/Tables','/Volumes/MaxDisk/Phoenix/Configuration']
target_folder = os.path.dirname(sys.argv[0]) + '/0924'


class copy_that(object):
    def __init__(self, source=None, target=None):
        self.source = source
        self.target = target
        self.getSerialNumber()
        self.mdir_folder()

    def copyFile(self):
        for i in self.source:
            if os.path.isdir(i) or os.path.isfile(i):
                if 'LoboMini' in i:
                    os.system('cp -rf %s %s' % (i, self.mkdir_target_lobo))
                if 'MaxDisk' in i and 'Tables' not in i: 
                    os.system('cp -rf %s %s' % (i, self.mkdir_target_maxdisk))
                if 'Tables' in i or 'Configuration' in i:
                    os.system('cp -rf %s %s' % (i, self.mkdir_target))    

    def getSerialNumber(self):
        self.serialnumber = commands.getoutput(
            'system_profiler SPHardwareDataType | grep "Serial Number" | sed \'s/.*: //\'')

    def mdir_folder(self):
        self.mkdir_target = self.check_folder_exist()
        self.mkdir_target_lobo = self.mkdir_target + '/Lobo'
        self.mkdir_target_maxdisk = self.mkdir_target + '/MaxDisk'
        os.mkdir(self.mkdir_target)
        os.mkdir(self.mkdir_target_lobo)
        os.mkdir(self.mkdir_target_maxdisk)

    def check_folder_exist(self):
        try:
            root = os.walk(self.target).next()[1]
            folder_list = []
            for i in root:
                if self.serialnumber in i:
                    folder_list.append(int(str(i).split('_')[1]))
            number = int(max(folder_list)) + 1
        except:
            number = 1

        print "\033[0;32m[" + self.serialnumber + '] verified finished times was : ' + str(number) + "\033[0;30m"
        return self.target + '/' + self.serialnumber + '_' + str(number)


if __name__ == '__main__':
    t = copy_that(source=source_file, target=target_folder)
    t.copyFile()
