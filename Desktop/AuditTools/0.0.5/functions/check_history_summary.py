#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/3上午9:53
# @Author   : Saseny Zhou
# @Site     : 
# @File     : check_history_summary.py
# @Software : PyCharm


from functions.path import *
from functions.json_file import *


def current_summary_check():
    try:
        config = read_json_file(os.path.join(resources, "config.json"))
        currentTime = time.strftime("%Y_%m_%d")
        xlsxFolder = os.path.join(result_xlsx_back_up_path, currentTime)
        log_collect_append.logger.debug(xlsxFolder)
        fileList = []
        try:
            fileList = [x for x in os.listdir(xlsxFolder) if str(x).endswith(".xlsx")]
        except:
            pass
        log_collect_append.logger.debug("History summary file count: %s" % str(len(fileList)))
        log_collect_append.logger.debug(fileList)

        return_dict = {}

        for i in fileList:
            product = str(i).split("_")[0]
            station_tmp = str(i).split("_")[1]
            for l in config["product-station-command"][product].keys():
                if str(station_tmp) == l:
                    station = l
                    break
                if str(station_tmp) == config["product-station-command"][product][l]["download"]["station"]:
                    station = config["product-station-command"][product][l]["download"]["station"]
                    break
            log_collect_append.logger.info(product)
            log_collect_append.logger.info(station)
            if return_dict.get(product, False) is False:
                return_dict[product] = []
            return_dict[product].append([station, os.path.join(xlsxFolder, i)])
            log_collect_append.logger.info([station, os.path.join(xlsxFolder, i)])
        log_collect_append.logger.info(return_dict)

        return return_dict
    except:
        return False


def set_double_list(list_):
    _list = []
    for i in list_:
        check = True
        for j in _list:
            if i == j:
                check = False
                break
        if check is True:
            _list.append(i)

    return _list
