#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/11/29上午8:48
# @Author   : Saseny Zhou
# @Site     : 
# @File     : tools_1.0.py
# @Software : PyCharm Community Edition


import optparse
from Config.plist import *
from HASH.hashTool import *
from Functions.decorator import *
from Functions.shell import *
from Functions.folder import *
from Functions.copy_file import *
from Functions.readcsv import *
from Functions.readexcel import *
from Functions.myThread import *
from Logs.copy_logs import *
import re
import multiprocessing

dir_path = os.path.dirname(sys.argv[0])
error_code_path = None
units_number_path = None


class CollectLog(object):
    def __init__(self, config_):
        self.config = config_
        self.serial_number = self.read_sn()
        self.path_road = self.path()
        create_folder(self.path_road)
        self.p = multiprocessing.Process(target=log_running, args=(self.dict_info(),))

    def run(self):
        self.p.start()

    def path(self):
        if self.config['define_path']['bool'] is False:
            path_road = os.path.join(dir_path, self.serial_number)
        else:
            path_road = os.path.join(self.config['define_path']['path'], self.serial_number)
        return path_road

    def read_sn(self):
        serial_number = None
        tb = re.compile(self.config['sn_read']['read_rule'])
        a, b = shell(self.config['sn_read']['cmd'])
        if a == 0:
            sn = tb.findall(str(b))
            if len(sn) > 0:
                serial_number = sn[0]
        return serial_number

    def dict_info(self):
        dict_ = self.config['collection_log']
        dict_['destination'] = self.path_road
        dict_['name'] = time.strftime("Logs-%Y-%m-%d-%H-%M-%S")
        dict_['sshpath'] = None
        dict_['targz'] = None
        return dict_


class CollectionData(object):
    def __init__(self, config_, error_code=error_code_path):
        self.scp_cmd = '/usr/local/bin/eos-scp eos:/private/var/logs/Earthbound/%s %s'
        self.config = config_
        self.error_code_path = error_code
        self.serial_number = self.read_sn()
        self.path_road = self.path()
        create_folder(self.path_road)

    def path(self):
        if self.config['define_path']['bool'] is False:
            path_road = os.path.join(dir_path, self.serial_number)
        else:
            path_road = os.path.join(self.config['define_path']['path'], self.serial_number)
        return path_road

    def read_sn(self):
        serial_number = None
        tb = re.compile(self.config['sn_read']['read_rule'])
        a, b = shell(self.config['sn_read']['cmd'])
        if a == 0:
            sn = tb.findall(str(b))
            if len(sn) > 0:
                serial_number = sn[0]
        return serial_number

    def read_dti(self):
        dti_version = 'None'
        a, obj = shell('cd %s; cat < %s' % (self.config['dti_read']['file_path'], self.config['dti_read']['file_name']))
        if a == 0:
            for i in obj:
                t = re.findall(self.config['dti_read']['read_rule'], i)
                if t:
                    dti_version = t[0]
                    break
        return dti_version

    @calculate()
    def run(self):
        mac_list = self.config['copy_files']['Mac_files'].keys()
        gos_list = self.config['copy_files']['gOS_files'].keys()
        for i in gos_list:
            if self.config['copy_files']['gOS_files'][i] is True:
                shell(self.scp_cmd % (i, self.path_road))
        for j in mac_list:
            if self.config['copy_files']['Mac_files'][j] is True:
                copy_file(j, self.path_road)
        write_txt(os.path.join(self.path_road, 'dti.txt'), self.read_dti())

    @calculate()
    def running(self):
        mac_list = self.config['copy_files']['Mac_files'].keys()
        gos_list = self.config['copy_files']['gOS_files'].keys()
        for i in gos_list:
            if self.config['copy_files']['gOS_files'][i] is True:
                shell(self.scp_cmd % (i, self.path_road))
        for j in mac_list:
            if self.config['copy_files']['Mac_files'][j] is True:
                copy_file(j, self.path_road)

        fail_file = os.path.join(self.path_road, 'failures.csv')
        fails = read_csv(fail_file, self.config['csv_read']['read_key'])
        name = self.config['xlsx_read']['sheet_name']
        column = self.config['xlsx_read']['column']
        station = self.config['xlsx_read']['station']
        station_column = self.config['xlsx_read']['station_column']
        errors = read_xlsx(self.error_code_path, station, station_column, name, column)
        self.compress(fails, errors)

    def compress(self, fials, codes):
        have = []
        not_yet = []
        dti = self.read_dti()

        for i in fials:
            done = False
            for j in codes:
                if i == j[0]:
                    done = True
                    have.append(str(int(j[1])))
            if done is False:
                not_yet.append(i)

        print '机器序列号:', self.serial_number
        print 'DTI 版本:', dti
        print 'Error Code:', have
        print '需增加:', not_yet

        for d in [self.serial_number, dti, have, not_yet]:
            write_txt(os.path.join(self.path_road, 'info.txt'), d)

        if self.config['open_result']:
            os.system('open %s' % os.path.join(self.path_road, 'info.txt'))


class Report(object):
    def __init__(self, path, config_, form_, tgz=False):
        self.path = path
        self.format = form_
        self.tgz = tgz
        self.config = config_
        self.files_list = find_file(self.path, self.format)

    def run(self):
        main_thread(self.files_list, self.config, dir_path, tgz=self.tgz)

    def running(self):
        main_thread(self.files_list, self.config, dir_path, tgz=self.tgz)


class FinalReport(object):
    def __init__(self, plist_path, unis_path=units_number_path):
        self.plist_path = plist_path
        self.units_path = unis_path

    def run(self):
        dict_info = read_plist(self.plist_path)
        unit_info = excel_read(self.units_path)

        file_name = dict_info.keys()

        for i in file_name:
            if '_' in i:
                dti = str(i).split('_')[1]
                file_path = os.path.join(dir_path, dti + '_' + time.strftime("%Y_%m_%d_%H_%M_%S") + '.csv')
            else:
                file_path = os.path.join(dir_path, 'final_' + time.strftime("%Y_%m_%d_%H_%M_%S") + '.csv')
            self.process(file_path, dict_info[i], unit_info)

    def process(self, result, dict_info, unit_info):
        final_report = []
        sou = dict_info
        fin = unit_info
        if sou is None or fin is None:
            print 'File wrong! Pls check.'
            sys.exit(1)
        for i in xrange(int(len(sou))):
            final = [str(int(i) + 1), sou[str(int(i) + 1)]['failure'], sou[str(int(i) + 1)]['times'], []]
            for j in sou[str(int(i) + 1)]['units']:
                write = False
                for l in fin:
                    if j in l[0]:
                        write = True
                        final[3].append('#' + str(l[1]))
                if write is False:
                    final[3].append(j)
            final_report.append(final)
        self.writecsv(result, final_report)

    def writecsv(self, final_result, final_report):
        writer = csv.writer(file(final_result, 'wb'))
        title = ['number', 'failure', 'times', 'units']
        writer.writerow(title)
        for i in final_report:
            writer.writerow(i)


def main():
    global config
    global error_code_path
    global units_number_path

    p = optparse.OptionParser()

    p.add_option("-a", action="store_true", dest="collection",
                 help="collection DTI info and files, then create SN folder and put in")
    p.add_option("-b", action="store_true", dest="report",
                 help="report burnin report, output error code and need add error code")
    p.add_option("-c", action="store_true", dest="config", help="write sample config.plist file")
    p.add_option("-d", action="store", dest="from_csv",
                 help="report plist report from failures.csv files")
    p.add_option("-e", action="store", dest="from_tgz",
                 help="report plist report from tgz files")
    p.add_option("-r", action="store", dest="report_plist",
                 help="report observation report from plist")
    p.add_option("-l", action="store_true", dest="collect_logs", help="enable collection logs")
    p.add_option("--config_file", action="store", type='string', dest="configfile",
                 help="provide config file without use internal config")
    p.add_option("--error_code", action="store", type='string', dest="errorfile",
                 help="provide error code file without do not check error code")
    p.add_option("--unit_number", action="store", type='string', dest="units",
                 help="provide units number file without do not check units number")
    p.add_option("-v", "--version", action="store_true", dest="version", help="show current command version")
    p.set_defaults(debug=False)

    (options, args) = p.parse_args()

    if options.configfile:
        config = read_plist(options.configfile)
        if config is False:
            print 'config file was wrong.'
            sys.exit(1)
        hash_check(config['check_sum'])

    if options.errorfile:
        error_code_path = options.errorfile

    if options.units:
        units_number_path = options.units

    if options.config:
        write_plist(os.path.join(dir_path, 'config.plist'), force=True)
        sys.exit(0)

    if options.version:
        print 'Version:', version
        sys.exit(0)

    if options.collect_logs:
        d = CollectLog(config)
        d.run()

    if options.collection:
        t = CollectionData(config, error_code_path)
        t.run()
        sys.exit(0)

    if options.report:
        f = CollectionData(config, error_code_path)
        f.running()
        sys.exit(0)

    if options.from_csv:
        p = Report(options.from_csv, config, form_='failures.csv')
        p.run()
        sys.exit(0)

    if options.from_tgz:
        k = Report(options.from_tgz, config, form_=config['test_logs']['format'], tgz=True)
        k.running()
        sys.exit(0)

    if options.report_plist:
        t = FinalReport(options.report_plist, units_number_path)
        t.run()
        sys.exit(0)


if __name__ == "__main__":
    main()
