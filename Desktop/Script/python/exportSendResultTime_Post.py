# -*- coding: utf-8 -*-
from fileProcess import *
import sys

q = queue.Queue(0)
NUM_WORKERS = 10
mylock = threading.Lock()


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
        doJob(job, worktype)

    def mainRun(self, list):
        for i in list:
            q.put(i)
        print("Job Qsize:", q.qsize())
        for x in range(NUM_WORKERS):
            MyThread(q, x).start()


def doJob(job, worktype):
    t.running(job, worktype)


class mytools(forLogCheck):
    def __init__(self, path=None, suffix=None, result=None):
        super(mytools, self).__init__()
        self.path = path
        self.suffix = suffix
        self.result = result

    def running(self, file, worktype):
        sn, folderpath, logpath = self.UNTGZFile(file)

        print('Starting  -- >> [%s]  -- Thread %i' % (sn, int(worktype)))
        if sn != None or folderpath != None or logpath != None:
            time1, a = self.readLogTime(logpath, 'Comm.Send.TestEnvInfo', 'Post.ntab')
            time2, b = self.readLogTime(logpath, 'Comm.Send.Results', 'Post.ntab')
            time3, c = self.readLogTime(logpath, 'Comm.Send.ParametricData', 'Post.ntab')
            time4, d = self.readLogTime(logpath, 'Comm.Send.BundleList', 'Post.ntab')
            ab = sn + ',' + str(time1) + ',' + str(time2) + ',' + str(time3) + ',' + str(time4)
            os.system('rm -rf %s' % folderpath)
            mylock.acquire()
            self.writeCsv(ab)
            mylock.release()
            print('Finished  -- >> [%s]  -- Thread %i' % (sn, int(worktype)))

    def writeCsv(self, string):
        if not os.path.isfile(self.result):
            ret = 'SerialNumber' + ',' + 'TestEnvInfo' + ',' + 'ResultsTime' + ',' + 'ParametricData' + ',' + 'BundleList'
            self.writefile(ret, self.result)
        self.writefile(string, self.result)

    def UNTGZFile(self, file):
        pathName = None
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
                return a
            elif failPath:
                a = serialnumber, pathName, failPath[0]
                return a
            else:
                os.system('rm -rf %s' % pathName)
                return [None, None, None]

        else:
            print(file + ': 文件路径不存在')


if __name__ == '__main__':
    t = mytools()
    t.suffix = '.tgz'
    t.path = input('请输入Log文件夹路径:')
    t.result = os.path.dirname(sys.argv[0]) + '/' + time.strftime("%Y_%m_%d_%H_%M_%S") + '_time.csv'
    list = t.findFile()
    for i in list:
        q.put(i)
    print("Job Qsize:", q.qsize())
    for x in range(NUM_WORKERS):
        MyThread(q, x).start()
