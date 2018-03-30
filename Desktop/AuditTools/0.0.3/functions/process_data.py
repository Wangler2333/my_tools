#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/2/28下午7:37
# @Author   : Saseny Zhou
# @Site     : 
# @File     : process_data.py
# @Software : PyCharm


from functions.path import *
from functions.json_file import *
from functions.shell import *

main_config_read = read_json_file(os.path.join(resources, "config.json"))


def get_data_from_gz(source_path, target_path):
    name = str(source_path).replace(".gz", "")
    rename = str(name) + ".csv"  # 更改后名称，以csv结尾
    if main_config_read.get("backup-data", False) is True:  # 是否备份数据，在主配置文件中配置
        create_folder(backup_path)
        current_time = time.strftime("_%Y_%m_%d_%H_%M_%S")
        target = os.path.join(backup_path, os.path.basename(name) + str(current_time) + ".gz")
        shutil.copy(source_path, target)
    code = shell("gzip -d %s" % source_path)  # 调用shell命令gzip用于解压gz文件
    if code == 0:
        os.rename(name, rename)
        shutil.copy(rename, target_path)
        os.remove(rename)  # 删除原文件
        return True
    else:
        return False


class DataProcess():
    def __init__(self, source_path, target_path):
        self.source = source_path
        self.target = target_path
        self.name = os.path.basename(self.source).replace(".gz", "")
        self.product = str(self.name).split("_")[0]
        self.station = str(self.name).split("_")[1]
        self.config = main_config_read["product-station-command"][self.product][self.station]

    def process(self):
        code = 1
        path = "None"
        os.system("rm -rf %s/*" % tmp_path)
        BOOL = get_data_from_gz(self.source, self.target)
        if BOOL is True:
            command = command_define_path + str(self.config["cmd-link"])
            explain = self.config["explain"]
            cmd = explain + " " + command + " " + os.path.join(self.target, self.name + ".csv")
            code = shell(cmd)
            if code == 0:
                path = self.backUp()

        return code, path

    def backUp(self):
        fileList = os.listdir(tmp_path)
        currentTime = time.strftime("%Y_%m_%d")
        zipFolder = os.path.join(result_zip_back_up_path, currentTime)
        xlsxFolder = os.path.join(result_xlsx_back_up_path, currentTime)
        create_folder(zipFolder)
        create_folder(xlsxFolder)
        return_folder = "None"
        print(fileList)
        for i in fileList:
            tmp = os.path.join(tmp_path, i)
            if str(tmp).endswith(".zip"):
                shutil.copy(tmp, zipFolder)
            if os.path.isdir(tmp):
                for j in os.listdir(tmp):
                    if "Summary_Report" in j:
                        shutil.copy(os.path.join(tmp, j), xlsxFolder)
                        return_folder = os.path.join(xlsxFolder, j)
        return return_folder
