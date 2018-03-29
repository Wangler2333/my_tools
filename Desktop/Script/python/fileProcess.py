# -*- coding: utf-8 -*-

import os
import re
import glob
import time
import threading
import queue
import sys


q = queue.Queue(0)
NUM_WORKERS = 10
mylock = threading.Lock()


'''
文件处理模块
解压文件: tgz  返回由元组(sn,解压文件夹,processlog路径)
文件写入: 提供要写入的 string 字符串，以及文件路径
'''


class forLogCheck(object):
    def __init__(self, filepath=None, suffix=None):
        self.path = filepath
        self.suffix = suffix
        self.returnList = []

    def findFile(self):
        try:
            findList = []
            fns = [os.path.join(root, fn) for root, dirs, files in os.walk(self.path) for fn in files]
            for f in fns:
                if os.path.isfile(f):
                    if self.suffix in f:
                        findList.append(f)
            return findList
        except IOError as o:
            print('IOError', o)

    def unTGZFile(self, fileList=None):
        '''
        :param fileList:    提供压缩文件路径 List
        :return:        返回元组List包含: SN, 解压文件路径, processlog路径
        '''

        if fileList == None:
            fileList = self.findFile()
        else:
            fileList = [fileList]

        returnList = []

        for file in fileList:
            if os.path.isfile(file):

                path = os.path.dirname(file)
                os.system('cd %s ; tar -zxf %s &>/dev/null' % (path, file))
                pathName = str(file).replace('.tgz', '')

                t = re.findall(r'C02[A-Z]\w{8}', os.path.basename(file))
                if len(t) > 0:
                    serialnumber = t[0]
                else:
                    serialnumber = 'None'

                passPath = glob.glob(pathName + '/*/processlog.plog')
                failPath = glob.glob(pathName + '/*/*/processlog.plog')

                if passPath:
                    a = serialnumber, pathName, passPath[0]
                    returnList.append(a)
                elif failPath:
                    a = serialnumber, pathName, failPath[0]
                    returnList.append(a)
                else:
                    os.system('rm -rf %s' % pathName)

                print('Process -> : %s' % serialnumber)
            else:
                print(file + ': 文件路径不存在')

        return returnList

    def writefile(self, string, path):
        try:
            f = open(path, 'a')
            f.write(str(string) + '\n')
            f.close()
        except:
            print('写入文件错误')

    def timeCheck(self, time_):
        try:
            timeArray = time.strptime(time_, "%Y/%m/%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
        except UnboundLocalError as p:
            print('UnboundLocalError', p)

    def unDgzLog(self, file):
        pass

    def doJob(self, job, worktype):
        pass

    def readLogTime(self, *parameter):
        '''
        :param parameter: 输入元组，第一个元素需为 要处理的文件，其他元素为文件中搜索的关键字.
        :return: 返回首个时间和末尾时间的时间差以及时间列表  [Log 时间格式: 2017/09/05 21:00:00]
        '''

        return_time = []
        running = True
        a = len(parameter)
        leftTime = None

        if not os.path.isfile(parameter[0]):
            print('第一个参数不是文件,请确认后再试.')
            running = False
        elif a < 2:
            print('参数不够,小于2个参数,请确认后再试.')
            running = False
        elif a > 5:
            print('参数数量过多,大于5个参数,请确认后再试.')
            running = False

        if running == True:
            f = open(parameter[0], 'r')
            f_obj = f.readlines()
            f.close()

            for i in f_obj:
                if a == 2:
                    if parameter[1] in i:
                        timeSamply = re.findall(r'\d{4}\/\d{2}\/\d{2} \d{2}\:\d{2}\:\d{2}', str(i.replace('\n', '')))
                        if timeSamply:
                            return_time.append(timeSamply[0])
                if a == 3:
                    if parameter[1] in i and parameter[2] in i:
                        timeSamply = re.findall(r'\d{4}\/\d{2}\/\d{2} \d{2}\:\d{2}\:\d{2}', str(i.replace('\n', '')))
                        if timeSamply:
                            return_time.append(timeSamply[0])
                if a == 4:
                    if parameter[1] in i and parameter[2] in i and parameter[3] in i:
                        timeSamply = re.findall(r'\d{4}\/\d{2}\/\d{2} \d{2}\:\d{2}\:\d{2}', str(i.replace('\n', '')))
                        if timeSamply:
                            return_time.append(timeSamply[0])
                if a == 5:
                    if parameter[1] in i and parameter[2] in i and parameter[3] in i and parameter[4] in i:
                        timeSamply = re.findall(r'\d{4}\/\d{2}\/\d{2} \d{2}\:\d{2}\:\d{2}', str(i.replace('\n', '')))
                        if timeSamply:
                            return_time.append(timeSamply[0])
            if len(return_time) >= 2:
                leftTime = int(self.timeCheck(return_time[-1])) - int(self.timeCheck(return_time[0]))
            return leftTime, return_time

    def exportSnWip(self, file):
        if os.path.isfile(file):
            f = open(file, 'r')
            f_obj = f.readlines()
            f.close()

            snList = []
            wipList = []

            for i in f_obj:
                sn = re.findall(r'C02[A-Z]\w{8}', i)
                wip = re.findall(r'<Primary_UnitID>(C02[A-Z]\w{8}\+\S+)</Primary_UnitID>', i)

                if len(sn) > 0:
                    for j in sn:
                        snList.append(j)

                if len(wip) > 0:
                    for p in wip:
                        wipList.append(p)

            return snList, wipList

        else:
            print('路径文件不存在，请检查')

    def setList(self, list):
        returnList = []
        temp = set(list)
        for i in temp:
            returnList.append(i)
        return returnList


class MyThread(threading.Thread):
    def __init__(self, input, worktype):
        self._jobq = input
        self._work_type = worktype
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self._jobq.qsize() > 0:
                self._process_job(self._jobq.get(), self._work_type)
            else:
                break

    def _process_job(self, job, worktype):
        self.doJob(job, worktype)

    def mainRun(self, list):
        for i in list:
            q.put(i)
        print("Job Qsize:", q.qsize())
        for x in range(NUM_WORKERS):
            MyThread(q, x).start()

    def doJob(self, job, worktype):
        pass


if __name__ == '__main__':
    pass
