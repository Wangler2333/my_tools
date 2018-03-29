# -*- coding: utf-8 -*-


import subprocess


class subprocess_load(object):
    def __init__(self, disk=None, test=None, cm=None, testsize='70', retestsize='1', recoverysize='80'):
        self.disk = str(disk)
        self.test = str(test)
        self.cm = str(cm)
        self.testsize = str(testsize) + 'g'
        self.retestsize = str(retestsize) + 'g'
        self.recoverysize = str(recoverysize) + 'g'

        self.disk_A = str(self.disk) + 's3'
        self.disk_B = str(self.disk) + 's4'
        self.disk_C = str(self.disk) + 's5'
        self.command_list()

    def running(self):
        for i in self.CMDDict.keys():
            a = self.CMDDict[i]
            if str(a) == '0':
                continue
            else:
                break

    def run_command(self, cmd):
        a = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while a.poll() == None:
            print(a.stdout.readline())
        return a.returncode

    def command_list(self):
        partitionDisk = 'sudo diskutil partitionDisk /dev/%s 1 GPTFormat hfs+ NoName 1G' % self.disk
        partition = 'sudo /usr/sbin/asr partition --target /dev/%s --testsize %s --retestsize %s --recoverysize %s' % (
            self.disk, self.testsize, self.retestsize, self.recoverysize)
        # coreDump = 'sudo diskutil resizeVolume /dev/%s 70g \%5361644d-6163-11AA-AA11-00306543ECAC\% KernelCore 1g' % self.disk_A
        eraseVolume = 'sudo diskutil eraseVolume hfs+ Apple_Boot /dev/%s' % self.disk_C
        unmount1 = 'sudo diskutil unmount force /dev/%s' % self.disk_C
        adjust = 'sudo asr adjust --target /dev/%s --settype apple_kfs' % self.disk_C
        unmount2 = 'sudo diskutil unmount force /dev/%s' % self.disk_B
        asr_bundle = 'sudo /usr/sbin/asr restore --target /dev/%s --source %s --erase --noprompt --puppetstrings --noverify' % (
            self.disk_A, self.test)
        unmount3 = 'sudo diskutil unmountDisk force /dev/%s' % self.disk
        mount = 'sudo diskutil mount /dev/%s' % self.disk_A
        rename = 'sudo diskutil rename /dev/%s %s' % (self.disk_A, self.disk)



        cm_copy = 'sudo ditto -rsrcFork %s /Volumes/%s' % (self.cm, self.disk)
        rename_back = 'sudo diskutil rename /dev/%s MaxDisk' % self.disk_A

        unmount4 = 'sudo diskutil unmountDisk force /dev/%s' % self.disk

        self.CMDList = ['partitionDisk', 'partition', 'eraseVolume', 'unmount1', 'adjust', 'unmount2', 'asr_bundle',
                        'unmount3', 'mount', 'rename', 'cm_copy', 'rename_back', 'Finished']
        self.CMDDict = {'partitionDisk': partitionDisk,
                        'partition': partition,
                        'eraseVolume': eraseVolume,
                        'unmount1': unmount1,
                        'adjust': adjust,
                        'unmount2': unmount2,
                        'asr_bundle': asr_bundle,
                        'unmount3': unmount3,
                        'mount': mount,
                        'rename': rename,
                        'cm_copy': cm_copy,
                        'rename_back': rename_back,
                        'Finished': unmount4
                        }
