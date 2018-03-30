#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/1下午2:48
# @Author   : Saseny Zhou
# @Site     : 
# @File     : summary_data.py
# @Software : PyCharm


from functions.path import *
from functions.json_file import *
import xlwt
import xlrd


def time_check(_time):
    time_ = str(_time) + " " + "00:00:00"
    try:
        time_array = time.strptime(time_, "%d/%m/%Y %H:%M:%S")
        time_stamp = int(time.mktime(time_array))
        return time_stamp
    except:
        return 'None'


def time_return(number):
    try:
        time_array = time.localtime(int(number))
        other_style = time.strftime("%d/%m/%Y", time_array)
        return other_style
    except:
        return 'None'


def excel_read(file_, sheet, header=True):
    list_ = []
    try:
        data = xlrd.open_workbook(file_)
        table = data.sheets()[sheet]
        nrows = table.nrows
        print(data, table, nrows)
        for i in range(0, nrows):
            if header is True:
                list_.append(table.row_values(i))
            if header is False and i > 0:
                list_.append(table.row_values(i))
        return list_
    except TypeError as e:
        return list_


def excel_write(list, total_list, path, from_, product):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Audit Report Summary')

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 22
    style = xlwt.XFStyle()
    style.pattern = pattern

    worksheet.write(0, 0, "%s_Audit_Summary" % product)

    worksheet.write(1, 0, "Report Date:")
    worksheet.write(1, 1, time.strftime("%Y-%m-%d"))

    worksheet.write(2, 0, "Date Source Date:")
    worksheet.write(2, 1, from_)
    worksheet.write(2, 2, time.strftime("%d/%m/%Y"))

    title = ['Station Name', 'Audit Freq', 'Radar No.', 'Audit Overlay Version', 'line', 'Audit Station QTY',
             'Pass Station QTY', 'Fail Station QTY', 'Audit Pass Rate', 'Audit Pass Time', 'Effective deadline',
             'Within Limit', 'Overdue']

    for l in range(len(title)):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 70
        style = xlwt.XFStyle()
        style.pattern = pattern
        worksheet.write(3, l, title[l], style)

    for i in range(len(list)):
        for j in range(len(list[i])):
            if j == 8:
                if int(str((list[i][8])).split('.')[0]) < 80:
                    pattern = xlwt.Pattern()
                    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    pattern.pattern_fore_colour = 2
                    style = xlwt.XFStyle()
                    style.pattern = pattern
                else:
                    pattern = xlwt.Pattern()
                    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    pattern.pattern_fore_colour = 1
                    style = xlwt.XFStyle()
                    style.pattern = pattern
            else:
                pattern = xlwt.Pattern()
                pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                pattern.pattern_fore_colour = 1
                style = xlwt.XFStyle()
                style.pattern = pattern
            worksheet.write(i + 4, j, str(list[i][j]), style)

    for a in total_list:
        name = a[1][1]
        if name == "Display RGBW (Color Test + WP Match)":
            name = "RGBW"
        try:
            worksheet_tmp = workbook.add_sheet(name)
            for b in range(len(a)):
                for c in range(len(a[b])):
                    if 'fail' == str(a[b][c]).lower() or 'audit_overdue' == str(a[b][c]).lower():
                        pattern = xlwt.Pattern()
                        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                        pattern.pattern_fore_colour = 2
                        style = xlwt.XFStyle()
                        style.pattern = pattern
                    elif 'pass' == str(a[b][c]).lower() or 'audit_withindeadline' == str(a[b][c]).lower():
                        pattern = xlwt.Pattern()
                        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                        pattern.pattern_fore_colour = 3
                        style = xlwt.XFStyle()
                        style.pattern = pattern
                    elif 'Marginal Pass'.lower() == str(a[b][c]).lower():
                        pattern = xlwt.Pattern()
                        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                        pattern.pattern_fore_colour = 5
                        style = xlwt.XFStyle()
                        style.pattern = pattern
                    elif b == 8:
                        pattern = xlwt.Pattern()
                        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                        pattern.pattern_fore_colour = 70
                        style = xlwt.XFStyle()
                        style.pattern = pattern
                    elif b < 8:
                        pattern = xlwt.Pattern()
                        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                        pattern.pattern_fore_colour = 9
                        style = xlwt.XFStyle()
                        style.pattern = pattern
                    else:
                        pattern = xlwt.Pattern()
                        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                        pattern.pattern_fore_colour = 1
                        style = xlwt.XFStyle()
                        style.pattern = pattern
                    worksheet_tmp.write(b, c, str(a[b][c]), style)
        except:
            pass
    workbook.save(path)


def read_summary_report(file, frequency, radar):
    tb = re.compile(r'\d{2}/\d{2}/\d{4}')
    date_list = []
    list_read = excel_read(file, 0)

    print(list_read)

    for i in list_read:
        for j in i:
            if tb.findall(str(j)):
                date_list.append(time_check(tb.findall(j)[0]))

    print(date_list)

    return_info = [
        str(list_read[1][1]),
        frequency,
        radar,
        str(list_read[1][4]),
        str(list_read[1][7]).replace('\"', '').replace('\'', '').replace('None', '').replace(',', '').replace('[',
                                                                                                              '').replace(
            ']', ''),
        str(int(list_read[4][1])),
        str(int(list_read[5][1])),
        str(int(list_read[5][4])),
        str(round(float(list_read[5][1]) / float(list_read[4][1]) * 100, 2)) + " %",
        time_return(min(date_list)),
        time_return(max(date_list)),
        str(int(list_read[6][1])),
        str(int(list_read[6][4]))
    ]

    return return_info, list_read


class SummaryData():
    def __init__(self, fileList):
        self.config = read_json_file(os.path.join(resources, "config.json"))["product-station-command"]
        self.dict = fileList
        self.storePath = data_path

    def run(self):
        self.divide()
        return True

    def divide(self):
        for i in self.dict.keys():
            self.merge_report(self.dict[i], i)

    def merge_report(self, dictInfo, product):
        summary_list = []
        total_list = []
        date_list = []
        current_date = time.strftime("%Y%m%d")
        folder_name = "_".join([product, current_date])
        result_folder = os.path.join(data_path, folder_name)
        create_folder(result_folder)
        file_list = dictInfo  # 适配前面更改  原先是 dictInfo.items()

        print(result_folder)
        print(file_list)

        if len(file_list) > 0:
            for i in file_list:
                frequency = self.config[product][i[0]]["download"].get("frequency", "None")
                radar = self.config[product][i[0]]["download"].get("radar number", "None")

                print(frequency, radar)
                print(i[1])

                read_result = read_summary_report(i[1], frequency, radar)
                os.system("rm -rf %s" % str(i[1]))          # 读取文件之后删除excel文件
                print(read_result)

                date_list.append(time_check(read_result[0][-3]))
                date_list.append(time_check(read_result[0][-4]))
                summary_list.append(read_result[0])
                total_list.append(read_result[1])

                print("------------------------")
                print(summary_list)
                print(total_list)
                print(date_list)
                print("------------------------")

            form_date = time_return(min(date_list))
            result_path = os.path.join(result_folder, "%s_Summary_Audit_Report_%s.xls" % (
                product, time.strftime("%Y_%m_%d_%H_%M_%S")))
            excel_write(summary_list, total_list, result_path, form_date, product)
            # os.system("cp -rf %s ~/Downloads" % result_path)  # 复制到 ~/Downloads 下
            return "Run Finished."
        else:
            return "No result file for read."

# listFile = {
#     "J80A":
#         {
#             "FACT": "/Volumes/Development/Design/App_Design/Tools_For_Audit/0.0.1/Resources/result/xlsx_back_up/2018_03_01/J80A_FACT_Audit_Summary_Report_Mar-01-2018.xlsx",
#             "WIFI-BT-COND": "/Volumes/Development/Design/App_Design/Tools_For_Audit/0.0.1/Resources/result/xlsx_back_up/2018_03_01/J80A_WIFI-BT-COND_FATP_Weekly_Audit_Summary_Report_Mar-01-2018.xlsx"
#         }
# }
#
# t = SummaryData(listFile)
# t.divide()
