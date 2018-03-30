#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/16下午4:37
# @Author   : Saseny Zhou
# @Site     : 
# @File     : observation_report.py
# @Software : PyCharm


from Functions.excel_read import *
from collections import OrderedDict


class ObservationReport():
    def __init__(self, configInfo, unitsInfo, additional):
        self.configInfo = configInfo["process"]
        self.unitsInfo = unitsInfo
        self.additional = additional

    def files_list(self, result):
        os.system("rm -rf %s" % result)
        files = find_file(self.additional["path"], "failures.csv")

        for i in files:
            sn = re.findall(self.configInfo["Serial Number"]["read rule"], str(i))
            if sn:
                serial_number = sn[0]
                path = os.path.split(str(i))[0]
                failures = os.path.join(path, "failures.csv")
                unit_info = os.path.join(path, "unit_info.csv")
                try:
                    units_info_read = file_read(unit_info)[1]
                    dti_info = str(units_info_read).split(",")[1]
                    rack_id = str(units_info_read).split(",")[2]
                except:
                    dti_info = "None"
                    rack_id = "None"
                fails = self.read_error_info(failures)
                self.write_result(serial_number, fails, dti_info, result, rack_id)

        final_json = read_json_file(result)
        self.report(self.write_unit_number(final_json))

        return 1

    def read_error_info(self, path):
        failures = file_read(path)
        rule = self.configInfo["failure read"]

        return_list = []
        for i in failures:
            tmp = str(i).split(",")
            if re.findall(r'^[A-Z]+$', str(tmp[0])):  # 需要更改 现在发现有 TIMEOUT
                result = ""
                for j in rule["combination"].items():
                    if str(j[0]) == "name":
                        info = str(tmp[j[1]]).replace(rule["replace"], "")
                    elif str(j[0]) == "states":
                        info = "(Exit code: " + str(tmp[j[1]]) + ")"
                    else:
                        info = str(tmp[j[1]])
                    result += " " + info
                    return_list.append(str(result).lstrip())

        return_list = [x for x in set(return_list) if "Exit code" in x]
        return return_list

    def write_result(self, sn, list_, dti, result_file, id):
        if not os.path.isfile(result_file):
            dict_info = {}
            dict_two = OrderedDict()
            dict_info[dti] = dict_two
            for i in range(len(list_)):
                number = str(int(i) + 1)
                failure = list_[i]
                times = 1
                units = [sn]
                for ll in self.configInfo["Special Request"]:
                    if ll in str(list_[i]):  # 妈蛋，str(i) 是整数转字符...
                        units = [str(sn) + " <" + str(id) + ">"]  # 列表...
                        print(units)
                dict_two[number] = {
                    'failure': failure,
                    'times': times,
                    'units': units
                }
            write_json_file(dict_info, result_file)

        else:
            dict_info = OrderedDict(read_json_file(result_file))
            new_dti = True
            print(dict_info.keys())
            for i in dict_info.keys():
                if dti == i:
                    new_dti = False
                    break
            if new_dti is False:
                _list_ = []
                keys = len(dict_info[dti])
                for d in dict_info[dti].keys():
                    _list_.append(dict_info[dti][d]['failure'])
                for i in list_:
                    if i in _list_:
                        for j in dict_info[dti].keys():
                            if i == dict_info[dti][j]['failure']:
                                dict_info[dti][j]['times'] += 1
                                tmp = sn
                                print(tmp)
                                for ll in self.configInfo["Special Request"]:
                                    if ll in str(i):
                                        tmp = str(sn) + " <" + str(id) + ">"
                                        print(tmp)
                                dict_info[dti][j]['units'].append(tmp)
                                dict_info[dti][j]['units'] = [x for x in set(dict_info[dti][j]['units'])]
                                dict_info[dti][j]['times'] = len(dict_info[dti][j]['units'])
                    else:
                        keys += 1
                        tmp = sn
                        for ll in self.configInfo["Special Request"]:
                            if ll in str(i):
                                tmp = str(sn) + " <" + str(id) + ">"
                                print(tmp)
                        dict_info[dti][str(keys)] = {
                            'failure': str(i),
                            'times': 1,
                            'units': [tmp]
                        }
            else:
                dict_two = OrderedDict()
                dict_info[dti] = dict_two
                for i in range(len(list_)):
                    number = str(int(i) + 1)
                    failure = list_[i]
                    times = 1
                    units = [sn]
                    for ll in self.configInfo["Special Request"]:
                        if ll in str(list_[i]):  # 妈蛋，str(i) 是整数转字符...
                            units = [str(sn) + " <" + str(id) + ">"]  # 列表...
                    dict_two[number] = {
                        'failure': failure,
                        'times': times,
                        'units': units
                    }
                write_json_file(dict_info, result_file)
            write_json_file(dict_info, result_file)

    def write_unit_number(self, dict_info):
        for i in dict_info:
            for j in (dict_info[i]):
                tmp = dict_info[i][j]["units"]
                tmp_ = []
                for l in tmp:
                    check = False
                    sn = re.findall(self.configInfo["Serial Number"]["read rule"], str(l))
                    number = self.unitsInfo.get(str(sn[0]), False)
                    if number is not False:
                        tmp_.append(str(l).replace(sn[0], str(number["number"])))
                        check = True
                    if check is False:
                        tmp_.append(str(l))
                dict_info[i][j]["units"] = tmp_
        return dict_info

    def report(self, dict_info):
        current = time.strftime("%Y_%m_%d_%H_%M_%S")
        title = ["No.", "Failure", "Fail Rate", "Units Info"]

        if len(dict_info) > 1:
            tt = ["DTI Info"]
            info = ["Qty"]
            for o in dict_info:  # 增加多个 DTI 出现的时候 输出 各 DTI 所收集的机器的数量
                tt.append(o)
                tmp_units = []
                for u in dict_info[o]:
                    tmp_units.extend(dict_info[o][u]["units"])
                tmp_units = [s for s in set(tmp_units)]
                info.append(len(tmp_units))
            write_csv([tt, info], os.path.join(self.additional["path"], "DTI_units_qty.csv"))

        for i in dict_info:
            file_name = os.path.join(self.additional["path"], str(i) + "_" + str(current) + ".csv")
            print(file_name)
            final = []
            final.append(title)
            for j in range(len(dict_info[i])):
                times = int(dict_info[i][str(j + 1)]["times"])
                rate = str(round(float(int(times) / int(self.additional["total"])), 2) * 100) + "%"
                tmp = [str(j + 1), dict_info[i][str(j + 1)]["failure"], rate, dict_info[i][str(j + 1)]["units"]]
                final.append(tmp)
            write_csv(final, file_name)
