########################################################################################################

# FACT Audit Script

# Version:1.0 2017-12-1

# 1.1 output raw extract, each station only include three last measurement

# 1.2 output Single_output_columns criteria

# 1.16 detailed excel report correct

# 1.17 correct overal excel report

# 1.19 Summary report output with background color setting

# 1.22 Validate 2 Group GU cases, J130A config added, plot is fine for 2Group

# 1.23 plot is fine for 2Group

# 1.30 adapted to Insight data format

########################################################################################################

# run script: python xxx.py xxx.csv

# input:

#   PDCA wipas audit raw data

#   add GU SN 

# output:

#   extract PFA raw data and FACT raw data(completed)

#   



#########################################################################################################

import pandas as pd

import numpy as np

from colorama import Fore, Back, Style



import matplotlib

import matplotlib.pyplot as plt

import matplotlib.ticker as plticker

import os

import platform

import datetime

from matplotlib.backends.backend_pdf import PdfPages

import json

import re

import logging

import shutil

from StyleFrame import StyleFrame

pd.options.mode.chained_assignment = None



from scipy.optimize import curve_fit





def extrapolate(df):

    def func(x, a, b, c, d):

        return a * (x ** 3) + b * (x ** 2) + c * x + d



    # Initial parameter guess, just to kick off the optimization

    guess = (0.5, 0.5, 0.5, 0.5)



    # Create copy of data to remove NaNs for curve fitting

    fit_df = df.dropna()



    # Place to store function parameters for each column

    col_params = {}



    # Curve fit each column

    for col in fit_df.columns:

        # Get x & y

        x = fit_df.index.astype(float).values

        y = fit_df[col].values

        # Curve fit column and get curve parameters

        params = curve_fit(func, x, y, guess)

        # Store optimized parameters

        col_params[col] = params[0]



    # Extrapolate each column

    for col in df.columns:

        # Get the index values for NaNs in the column

        x = df[pd.isnull(df[col])].index.astype(float).values

        # Extrapolate those points with the fitted function

        df[col][x] = func(x, *col_params[col])

    return df





class FACT_AuditTool:

    def __init__(self):

        self.load_global_config()



    def load_global_config(self):

        script_path = os.path.split(os.path.realpath(__file__))[0]

        with open(os.path.join(script_path, 'FACT_config.json')) as config_file:

            self.config = json.load(config_file)



    def has_limit(self, col):

        return not np.isnan(np.float(self.source.ix[4, col])) and not np.isnan(np.float(self.source.ix[5, col]))



    def lineName(self, stationName):

        if re.search(r'-([A-Z][0-9]+)_',stationName) != None :

            return re.search(r'-([A-Z][0-9]+)_',stationName).group(1)

        else:

            print('Station ignored %s :', stationName)





    def FR_headers(self, headers):

        new_FR_headers = []

        for header in headers:

            FR_freq = re.search(r'Spectrum@(\d+)', header).group(1)

            new_FR_headers.append(FR_freq)

        return new_FR_headers



    def load(self, filename):

        work_dir, short_filename = os.path.split(filename)

        self.base_dir = work_dir

        short_filename_without_ext, ext = os.path.splitext(short_filename)

        self.work_dir = os.path.join(work_dir, short_filename_without_ext)

        if not os.path.exists(self.work_dir):

            os.makedirs(self.work_dir)

        logging.info('Loading file.')

        # read orginal file, convert str to lower letter

        if 'xls' in ext.lower():

            self.source = pd.read_excel(filename, header=None)

        if 'csv' in ext.lower():

            # self.source = pd.read_csv(filename, header=None, dtype=np.str)

            first_row = pd.read_csv(filename, header=None, nrows=1)

            other_rows = pd.read_csv(filename, header=1, dtype=np.str)

            first_row.columns = other_rows.columns[0:len(first_row.columns)]

            s = pd.Series(first_row.iloc[0], index=other_rows.columns)

            self.source = pd.DataFrame(columns=other_rows.columns)

            self.source = self.source.append(s, ignore_index=True)

            s = pd.Series(self.source.columns, index=other_rows.columns)

            self.source = self.source.append(s, ignore_index=True)

            self.source = self.source.append(other_rows, ignore_index=True)



        logging.info('File Loaded.')

        # read .csv file

        # self.version = self.source.iloc[0, 1].replace(' Version:', '').strip()

        self.station = self.source.iloc[0, 0]

        self.auditoverlay=self.source.iloc[0,1]



        self.project_name = self.source.iloc[7, 1]

        self.site = self.source.iloc[7, 0]        

        self.source.columns = self.source.iloc[1, :]

        self.source = self.source.iloc[7:, :]



        self.single_output_columns = []

        self.multiple_output_columns = []

        self.output_columns = []

        self.columns_dict = dict()



        self.test_categories = []



        for test in self.config["Tests_FR"]:

            if test['Project'] != self.project_name:

                continue

            if test["Category"] not in self.test_categories:

                self.test_categories.append(test["Category"])

            cols = []

            for filter in test["Filters"]:

                for col in self.source.columns:

                    if filter in col:

                        cols.append(col)

                        if (col not in self.multiple_output_columns):

                            self.multiple_output_columns.append(col)

                        if (col not in self.output_columns):

                            self.output_columns.append(col)

            self.columns_dict[test["ID"]] = cols



        for test_seal in self.config["Tests_Seal"]:



            if test_seal['Project'] != self.project_name:

                continue

            if test_seal["Category"] not in self.test_categories:

                self.test_categories.append(test_seal["Category"])

            cols = []

            for filter in test_seal["Filters"]:

                for col in self.source.columns:

                    if filter in col:

                        cols.append(col)

                        if (col not in self.multiple_output_columns):

                            self.multiple_output_columns.append(col)

                        if (col not in self.output_columns):

                            self.output_columns.append(col)

            self.columns_dict[test_seal["ID"]] = cols



        for test_single in self.config["Tests_Single"]:

            if test_single['Project'] != self.project_name:

                continue

            if test_single["Category"] not in self.test_categories:

                self.test_categories.append(test_single["Category"])

            cols = []

            for unit in test_single["Units"]:

                for col in self.source.columns:

                    if unit["Filter"].strip() == col.strip():

                        cols.append(col)

                        if (col not in self.single_output_columns):

                            self.single_output_columns.append(col)

                        if (col not in self.output_columns):

                            self.output_columns.append(col)

            self.columns_dict[test_single["ID"]] = cols



        # logging.info('Version : %s' % self.version)

        logging.info('Project : %s' % self.project_name)

        logging.info('SMT_StationName: %s' % self.station)

        # logging.info('Count of txPower columns : %d' % len(self.txpower_columns))

        # logging.info('Count of pathloss columns : %d' % len(self.pathloss_columns))



    def output_FACT_rawdata(self):

        self.data = self.source

        self.data['Line Name'] = self.data['Station ID'].map(lambda x: self.lineName(x))

        lineNames = self.data['Line Name'].drop_duplicates()

        StationNames = self.data['Station ID'].drop_duplicates()

        print(StationNames)

        groups = []

        # df_Grape=pd.DataFrame(columns=['SerialNumber','Station ID','Test Pass/Fail Status','StartTime']+self.output_columns)

        # df_Grape=pd.DataFrame(columns=self.output_columns)

        self.df_FACT = pd.DataFrame()



        for group in self.config["GlobalGroupConfig"]:

            if group['Project'] == self.project_name:

                groups.append(group)

        print(groups)



        group_index=1

        #stations = []

        #stationNames = []



        for group in groups:

            serial_numbers = group["SerialNumbers"]



            logging.info('Group%d[%s] ' % (group_index,' '.join(serial_numbers)))

            stations = []

            stationNames = []



            #for stationName in list(self.source.iloc[7:, :].loc[:, 'Station ID'].drop_duplicates()):

            for stationName in StationNames:

                rows = self.source[self.source['Station ID'] == stationName]

                print(stationName)

                rows = rows[rows['SerialNumber'].isin(serial_numbers)]

                if rows.shape[0] > 2:

                    logging.warning('SN Count>3, last 3 selected. Station : %s' % (stationName))

                    for serial_number in serial_numbers:

                        r = rows[rows['SerialNumber'] == serial_number]

                        r['StartTime'] = pd.to_datetime(r['StartTime']).values

                        if r.shape[0] > 1:

                            r = r.sort_values(['StartTime'], ascending=False)

                            rows = rows.drop(r.index[1:])

                    stations.append((stationName, rows))

                    stationNames.append((stationName))

                self.df_FACT = self.df_FACT.append(rows, ignore_index=True)

                if rows.shape[0] < 3:

                    logging.warning('SN Missing. Station : %s' % (stationName))

                    continue

                logging.info('Station Amount : %d' % (len(stations)))

            group_index+=1            



        ###########################################################################################################################################################################

        # Raw data extraction

        writer = pd.ExcelWriter(

            os.path.join(self.work_dir, '%s_FACT_Audit_Data_Extract_%s.xlsx' % (self.project_name, datetime.datetime.now(

            ).strftime('%b-%d-%Y'))), engine='xlsxwriter')

        sheet_name = 'PFA data Extract'

        self.df_FACT.to_excel(writer, sheet_name=sheet_name, index=False, header=True)

        workbook = writer.book

        worksheet = writer.sheets[sheet_name]



        self.df_FACT_Output = self.df_FACT.loc[:, ['SerialNumber', 'Station ID', 'Test Pass/Fail Status',

                                                   'StartTime'] + self.output_columns]

        self.df_FACT_Output.to_csv(

            os.path.join(self.work_dir, self.project_name + '_' + self.station + '_' + 'FACT_Extract_JMP.csv'),

            index=None)

        logging.info('%s_FACT_Extract_JMP.csv' % self.station)



        sheet_name = 'FACT Extract'

        self.df_FACT_Output.to_excel(writer, sheet_name=sheet_name, index=False, header=True)

        workbook = writer.book

        worksheet = writer.sheets[sheet_name]



        Min_Audit_Date = min(self.df_FACT_Output['StartTime'])

        Max_Audit_Date = max(self.df_FACT_Output['StartTime'])







        ###########################################################################################################################################################################



        writer.save()



        ########################################################################################################################################################

        # Output audit results detail report in excel format

        writer = pd.ExcelWriter(os.path.join(self.work_dir, '%s_%s_Audit_Results_Report_%s.xlsx' % (self.project_name, self.station,datetime.datetime.now().strftime('%b-%d-%Y'))), engine='xlsxwriter')



        #writer = pd.ExcelWriter(os.path.join(self.work_dir, '%s_%s_Audit_Results_Report_%s.xlsx' % (self.project_name, self.station,datetime.datetime.now().strftime('%b-%d-%Y'))), engine='xlsxwriter')





        overall_columns = ['Group', 'Line', 'Station ID', 'Audit pass time', 'Effective deadline',

                           'Overall result'] + self.test_categories

        detail_columns = [' Group ', ' Line ', ' Station ID ']

        NOTdetail_columns = [' Group ', ' Line ', ' Station ID ']



        for category in self.test_categories:

            for test in self.config["Tests_FR"]:

                if test['Project'] != self.project_name:

                    continue

                if test['Category'] != category:

                    continue

                detail_columns += self.columns_dict[test["ID"]]

                #NOTdetail_columns += self.columns_dict[test["ID"]]

                detail_columns.append(test["ID"])

                NOTdetail_columns.append(test["ID"])

            for test in self.config["Tests_Seal"]:

                if test['Project'] != self.project_name:

                    continue

                if test['Category'] != category:

                    continue

                detail_columns += self.columns_dict[test["ID"]]

                detail_columns.append(test["ID"])

                NOTdetail_columns.append(test["ID"])



            for test in self.config["Tests_Single"]:

                if test['Project'] != self.project_name:

                    continue

                if test['Category'] != category:

                    continue

                detail_columns += self.columns_dict[test["ID"]]

                NOTdetail_columns+= self.columns_dict[test["ID"]]



                # detail_columns.append(test["ID"])

            detail_columns.append(category)



        # for test in self.config["Tests_FR"]+self.config["Tests_Seal"]+self.config["Tests_Single"]:

        #     if test['Project'] != self.project_name:

        #         continue

        #     detail_columns += self.columns_dict[test["ID"]]

        #     detail_columns.append(test["ID"])

        df_NEWOUTPUT_overall = pd.DataFrame(columns=overall_columns)

        df_NEWOUTPUT_detail = pd.DataFrame()

        df_NEWOUTPUT_detail = df_NEWOUTPUT_detail.append(pd.Series(detail_columns), ignore_index=True)

        df_NEWOUTPUT_NOTdetail = pd.DataFrame()

        df_NEWOUTPUT_NOTdetail = df_NEWOUTPUT_NOTdetail.append(pd.Series(NOTdetail_columns), ignore_index=True)

        

        groupIndex = 1

        for group in groups:

            currentGroup = 'Group' + str(groupIndex)

            serial_numbers = group["SerialNumbers"]

            #data = all_diff[self.df_FACT['SerialNumber'].isin(serial_numbers)]

            #data_Seal = all_data[self.df_FACT['SerialNumber'].isin(serial_numbers)]

            self.Group_data = self.df_FACT_Output[self.df_FACT_Output['SerialNumber'].isin(serial_numbers)]

            self.Group_data_Seal = self.df_FACT_Output[self.df_FACT_Output['SerialNumber'].isin(serial_numbers)]





            # data_mean = data.mean()

            # data = data.groupby(by=['Station ID']).mean()

            # data = data.sub(data_mean)

            # data.columns = map(int,self.FR_headers(data.columns))

            # dataT = data.T

            all_data = self.Group_data[self.output_columns].astype(np.float).dropna()

            all_mean = all_data.mean()

            all_diff = all_data.sub(all_mean)



            all_diff["SerialNumber"] = self.Group_data["SerialNumber"]

            all_diff['Station ID'] = self.Group_data['Station ID']

            all_diff['StartTime'] = self.Group_data['StartTime']



            all_data["SerialNumber"] = self.Group_data["SerialNumber"]

            all_data['Station ID'] = self.Group_data['Station ID']

            all_data['StartTime'] = self.Group_data['StartTime']







            for station in  self.Group_data['Station ID'].drop_duplicates():

                # for station in data.loc[:, 'Station ID'].drop_duplicates():



                data_station = all_diff[self.Group_data['Station ID'] == station]

                data_Seal_station = all_data[self.Group_data_Seal['Station ID'] == station]

                

                data_station['StartTime'] = pd.to_datetime(data_station['StartTime'])

                data_station = data_station.sort_values(['StartTime'],ascending=False)

                #now = data_station['StartTime'].iloc[0]







                now=pd.to_datetime(data_station['StartTime']).iloc[0]

                #deadline = now

                

                deadline = now + datetime.timedelta(days=7)

                row = [currentGroup, self.lineName(station), station, now.strftime('%d/%m/%Y'),

                       deadline.strftime('%d/%m/%Y'), ""]

                row_detail = [currentGroup, self.lineName(station), station]

                row_NOTdetail = [currentGroup, self.lineName(station), station]



                for category in self.test_categories:

                    result = 'Pass'

                    for test in self.config["Tests_FR"]:

                        if test['Project'] != self.project_name:

                            continue

                        if test['Category'] != category:

                            continue

                        data_test = data_station[self.columns_dict[test["ID"]]].astype(np.float).mean().dropna()



                        data_test.index = map(int, self.FR_headers(data_test.index))



                        df_limit = pd.DataFrame(test["Limits"])

                        df_limit.index = df_limit.iloc[:, 0]

                        df_limit = df_limit.iloc[:, 1:]

                        df_limit.columns = ['MIN', 'MAX', 'COFMIN', 'COFMAX']



                        new_index=[]

                        for i in data_test.index:

                            if i not in new_index and i < np.max(df_limit.index.values) and i > np.min(df_limit.index.values):

                                new_index.append(i)

                        for i in df_limit.index:

                            if i not in new_index:

                                new_index.append(i)

                        new_index.sort();

                        df_limit = df_limit.reindex(new_index)

                        df_limit = df_limit.interpolate(method='index')

                        # df_limit = extrapolate(df_limit)

                        local_result = 'Pass'

                        for index in data_test.index:

                            if index in df_limit.index:

                                if data_test.loc[index] < df_limit.loc[index, 'COFMIN'] or data_test.loc[index] >  df_limit.loc[index, 'COFMAX']:

                                    if local_result == 'Pass' or local_result=='Marginal Pass':

                                        local_result = 'Fail'

                                    if result == 'Pass' or result == 'Marginal Pass':

                                        result = 'Fail'

                                if data_test.loc[index] < df_limit.loc[index, 'MIN'] or data_test.loc[index] > df_limit.loc[index, 'MAX']:

                                    if local_result == 'Pass':

                                        local_result = 'Marginal Pass'

                                    if result == 'Pass':

                                        result = 'Marginal Pass'

                            row_detail.append('%.3f'%data_test.loc[index])

                        row_NOTdetail.append(local_result)

                        row_detail.append(local_result)

                        #row_NOTdetail.append(local_result)



                    for test in self.config["Tests_Seal"]:

                        if test['Project'] != self.project_name:

                            continue

                        if test['Category'] != category:

                            continue



                        data_test = data_Seal_station[self.columns_dict[test["ID"]]].astype(np.float).mean()



                        data_test.index = map(int, self.FR_headers(data_test.index))



                        df_limit = pd.DataFrame(test["Limits"])

                        df_limit.index = df_limit.iloc[:, 0]

                        df_limit = df_limit.iloc[~df_limit.index.duplicated(keep='first'), 1:]

                        df_limit.columns = ['MIN', 'MAX']

                        new_index=[]

                        for i in data_test.index:

                            if i not in new_index and i < np.max(df_limit.index.values) and i > np.min(df_limit.index.values):

                                new_index.append(i)

                        for i in df_limit.index:

                            if i not in new_index:

                                new_index.append(i)

                        new_index.sort();

                        df_limit = df_limit.reindex(new_index)

                        df_limit = df_limit.interpolate(method='index')

                        local_result = 'Pass'

                        for index in data_test.index:

                            if index in df_limit.index:



                                if data_test.loc[index] < df_limit.loc[index, 'MIN'] or data_test.loc[index] > df_limit.loc[

                                    index, 'MAX']:

                                    local_result = 'Fail'

                                    if result == 'Pass':

                                        result = 'Fail'

                            row_detail.append('%.3f'%data_test.loc[index])

                        row_NOTdetail.append(local_result)

                        row_detail.append(local_result)



                    for test in self.config["Tests_Single"]:

                        if test['Project'] != self.project_name:

                            continue

                        if test['Category'] != category:

                            continue

                        for unit in test["Units"]:



                            data_test = data_station[unit["Filter"]].astype(np.float).mean()

                            limit = pd.Series(unit["Limit"], index=["MIN", "MAX", "COFMIN", "COFMAX"])

                            local_result = 'Pass'



                            if data_test < limit.loc['MIN'] or data_test > limit.loc['MAX']:

                                local_result = 'Marginal Pass'

                                if result == 'Pass':

                                    result = 'Marginal Pass'



                            if data_test < limit.loc['COFMIN'] or data_test > limit.loc['COFMAX']:

                                local_result = 'Fail'

                                if result == 'Pass' or result == 'Marginal Pass':

                                    result = 'Fail'



                            row_NOTdetail.append(local_result+"/"+'%.3f'%data_test)

                            row_detail.append(local_result+"/"+'%.3f'%data_test)

                        # row_detail.append(data_test)

                        # row_detail.append("")

                    row.append(result)

                    row_detail.append(result)

                    #row_NOTdetail.append(result)

                overall_result = 'Pass'

                for i in range(6, len(overall_columns)):

                    if row[i] == 'Marginal Pass' and overall_result == 'Pass':

                        overall_result = 'Marginal Pass'

                    if row[i] == 'Fail':

                        overall_result = 'Fail'

                row[5] = overall_result

                df_NEWOUTPUT_overall = df_NEWOUTPUT_overall.append(pd.Series(row, index=overall_columns),ignore_index=True)

                df_NEWOUTPUT_detail = df_NEWOUTPUT_detail.append(pd.Series(row_detail), ignore_index=True)

                df_NEWOUTPUT_NOTdetail = df_NEWOUTPUT_NOTdetail.append(pd.Series(row_NOTdetail), ignore_index=True)

            groupIndex += 1

        sheet_name = 'Overall Audit Report'

        df_NEWOUTPUT_overall = df_NEWOUTPUT_overall.groupby(by=['Group', 'Line', 'Station ID']).first()



        #df_NEWOUTPUT_overall_Auto= StyleFrame(df_NEWOUTPUT_overall)

        #df_NEWOUTPUT_overall_Auto.to_excel(excel_writer=writer, row_to_add_filters=0, columns_and_rows_to_freeze='B2')





        df_NEWOUTPUT_overall.to_excel(writer, sheet_name=sheet_name, index=True, header=True)



        workbook = writer.book

        worksheet = writer.sheets[sheet_name]

        green_color = workbook.add_format({'bg_color': '#00FF00'})

        yellow_color = workbook.add_format({'bg_color': 'yellow'})

        red_color = workbook.add_format({'bg_color': '#FF0000'})



        worksheet.conditional_format('F2:U227',{'type': 'text', 'criteria': 'begins with', 'value': 'Pass', 'format': green_color})

        worksheet.conditional_format('F2:U227',{'type': 'text', 'criteria': 'begins with', 'value': 'Fail', 'format': red_color})

        worksheet.conditional_format('F2:U227',{'type': 'text', 'criteria': 'begins with', 'value': 'Marginal Pass', 'format': yellow_color})







        sheet_name = 'Audit Report Breakdown'

        df_NEWOUTPUT_NOTdetail = df_NEWOUTPUT_NOTdetail.groupby(by=[0, 1, 2]).first()

        df_NEWOUTPUT_NOTdetail.to_excel(writer, sheet_name=sheet_name, index=True, header=True)

 

        workbook = writer.book

        worksheet = writer.sheets[sheet_name]

        green_color = workbook.add_format({'bg_color': '#00FF00'})

        yellow_color = workbook.add_format({'bg_color': 'yellow'})

        red_color = workbook.add_format({'bg_color': '#FF0000'})



        worksheet.conditional_format('D2:AL227',{'type': 'text', 'criteria': 'begins with', 'value': 'Pass', 'format': green_color})

        worksheet.conditional_format('D2:AL227',{'type': 'text', 'criteria': 'begins with', 'value': 'Fail', 'format': red_color})

        worksheet.conditional_format('D2:AL227',{'type': 'text', 'criteria': 'begins with', 'value': 'Marginal Pass', 'format': yellow_color})







        sheet_name = 'Audit Detailed Calculation'

        df_NEWOUTPUT_detail = df_NEWOUTPUT_detail.groupby(by=[0, 1, 2]).first()

        df_NEWOUTPUT_detail.to_excel(writer, sheet_name=sheet_name, index=True, header=True)



        workbook = writer.book

        worksheet = writer.sheets[sheet_name]

        green_color = workbook.add_format({'bg_color': '#00FF00'})

        yellow_color = workbook.add_format({'bg_color': 'yellow'})

        red_color = workbook.add_format({'bg_color': '#FF0000'})



        worksheet.conditional_format('D2:AHW227',{'type': 'text', 'criteria': 'begins with', 'value': 'Pass', 'format': green_color})

        worksheet.conditional_format('D2:AHW227',{'type': 'text', 'criteria': 'begins with', 'value': 'Fail', 'format': red_color})

        worksheet.conditional_format('D2:AHW227',{'type': 'text', 'criteria': 'begins with', 'value': 'Marginal Pass', 'format': yellow_color})



        writer.save()



        logging.info('%s Detailed Audit Report print ' % (self.station))





        ########################################################################################################################################################

        #Calculation for summary report (Audit Chamber QTY, Audit Pass/Fail %)

        pass_QTY=[]

        Marginal_pass_QTY=[]

        fail_QTY=[]

        Result_Columns=df_NEWOUTPUT_overall['Overall result']

        QTY_Chamber=len(Result_Columns)

        print(QTY_Chamber)

        for result in Result_Columns:

            if result=='Pass':

                pass_QTY.append(result)

            if result=='Marginal Pass':

                Marginal_pass_QTY.append(result)

            if result=='Fail':

                fail_QTY.append(result)



        Overdue_QTY=[]

        Within_Deadline_QTY=[]

        current_time=datetime.datetime.now().strftime('%d/%m/%Y')

        deadlines=df_NEWOUTPUT_overall['Effective deadline']

        for deadline in deadlines:

            if current_time<=deadline:

                Within_Deadline_QTY.append(deadline)

            if current_time>deadline:

                Overdue_QTY.append(deadline)





        logging.info('%s Audit station Status Calculation ' % (self.station))



        ########################################################################################################################################################

        #Final Audit Summary report published with background color setting

        writer = pd.ExcelWriter(os.path.join(self.work_dir, '%s_%s_Audit_Summary_Report_%s.xlsx' %(self.project_name,self.station,datetime.datetime.now(

        ).strftime('%b-%d-%Y'))), engine='xlsxwriter')

        sheet_name = 'Sheet1'

        df_header = pd.DataFrame()

        s = pd.Series(['General INFO'])

        df_header=df_header.append(s,ignore_index=True)

        s = pd.Series(['Staion Name:',self.station,' ']+['Audit Overlay:',self.auditoverlay,' ']+['Audit LineName:',list(set(lineNames))])

        df_header=df_header.append(s,ignore_index=True)



        s = pd.Series([''])

        df_header=df_header.append(s,ignore_index=True)   

        s = pd.Series(['Audit Status'])

        df_header=df_header.append(s,ignore_index=True)               

        s=pd.Series(['Audit Station QTY:',QTY_Chamber])

        df_header=df_header.append(s,ignore_index=True)

        s=pd.Series(['Audit Pass Station QTY:',len(pass_QTY),' ']+['Audit Fail Station QTY:',len(fail_QTY),' ']+['Audit Marginal Pass Station QTY:',len(Marginal_pass_QTY)])

        df_header=df_header.append(s,ignore_index=True)        

        s=pd.Series(['Within Deadline QTY:',len(Within_Deadline_QTY),' ']+['Overdue QTY:',len(Overdue_QTY)])

        df_header=df_header.append(s,ignore_index=True)            



        #s=pd.Series(['Audit Pass QTY:',len(Audit_overall_Result=='PASS')])

        df_header.to_excel(writer, sheet_name=sheet_name,index=False,header=False)

        df_NEWOUTPUT_overall.to_excel(writer,sheet_name=sheet_name,startrow=8)

        rows,cols = df_NEWOUTPUT_overall.shape

        workbook = writer.book

        worksheet = writer.sheets[sheet_name]

        green_color = workbook.add_format({'bg_color': '#00FF00'})

        yellow_color = workbook.add_format({'bg_color': 'yellow'})

        red_color = workbook.add_format({'bg_color': '#FF0000'})



        worksheet.conditional_format('F10:P27',{'type': 'text', 'criteria': 'begins with', 'value': 'Pass', 'format': green_color})

        worksheet.conditional_format('F10:P27',{'type': 'text', 'criteria': 'begins with', 'value': 'Fail', 'format': red_color})

        worksheet.conditional_format('F10:P27',{'type': 'text', 'criteria': 'begins with', 'value': 'Marginal Pass', 'format': yellow_color})



        writer.save()

        logging.info('%s Audit Summary Report Generation ' % (self.station))



        ########################################################################################################################################################

        # Plot Summary report

        pp = PdfPages(os.path.join(self.work_dir, '%s_%s_Audit Summary_%s.pdf' % (

        self.project_name, self.station, datetime.datetime.now(

        ).strftime('%b-%d-%Y'))))

        fig = plt.figure(figsize=(16, 9))

        plt.axis('off')

        plt.text(0.1, 0.7, self.project_name + ' ' + self.station + ' Audit Summary Report', fontsize=40)

        plt.text(0.2, 0.5, 'Report Generation Date:  ' + datetime.datetime.now().strftime('%b-%d-%Y'), fontsize=25)

        plt.text(0.25, 0.1, 'Audit Data Source: From ' + Min_Audit_Date + ' To ' + Max_Audit_Date, fontsize=15)



        pp.savefig()



        ########################################################################################################################################################



        # plot Test_FR(including MicFR and SpeakerFR plot)

        group_index = 1

        for group in groups:

            for test in self.config["Tests_FR"]:

                if test['Project'] != self.project_name:

                    continue

                serial_numbers = group["SerialNumbers"]

                self.data_Group = self.df_FACT[self.df_FACT['SerialNumber'].isin(serial_numbers)]

                data_extract = self.data_Group[self.columns_dict[test["ID"]]].astype(np.float)

                data_extract['Station ID'] = self.data_Group['Station ID']

                overall_mean = data_extract.mean()

                data_extract = data_extract.groupby(["Station ID"]).mean()

                data_diff = data_extract.sub(overall_mean)

                data_extract.columns = map(int, self.FR_headers(data_extract.columns))

                data_diff.columns = map(int, self.FR_headers(data_diff.columns))

                data_extract = data_extract.sort_index(axis=1, ascending=True)

                data_diff = data_diff.sort_index(axis=1, ascending=True)

                fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(16, 14));

                ax[0].set_xticks(data_extract.columns)



            # plt.grid()



            # all_mean=data_extract.mean()

            # all_mean.index=['Overall Mean']



            # overall_mean.plot(ax=ax[0],logx=True,linestyle='--',linewidth=3.0,sharex=True)

                data_extract.T.plot(ax=ax[0], logx=True)

                tmp = pd.DataFrame(test["Limits"])

                tmp.index = tmp.iloc[:, 0]

                tmp = tmp.iloc[:, 1:]

                tmp.columns = ['MIN', 'MAX', 'COFMIN', 'COFMAX']

                tmp.plot(ax=ax[1], logx=True, linestyle='--', linewidth=3.0, sharex=True)



                data_diff.T.plot(ax=ax[1], logx=True)



                ax[0].grid('on', which='both', axis='both')

                ax[1].grid('on', which='both', axis='both')



                ax[0].set_xlabel(test["ID"] + ' Freq (Hz)', fontsize=20)

                ax[1].set_xlabel(test["ID"] + ' Freq (Hz)', fontsize=20)

                title = self.station + '_Group'+str(group_index)+ '_' + test["ID"]

                filename = '%s' % self.project_name + '_' + title + '.pdf'

                plt.suptitle(title, fontsize=30)

                ax[0].legend(shadow=True, fontsize=6, loc='upper left')

                ax[1].legend(shadow=True, fontsize=6, loc='upper left')

                plt.savefig(os.path.join(self.work_dir, filename), dpi=200)

                pp.savefig()



                logging.info('%s Group %s  %s Plot Generation' % (self.station, group_index, test["ID"]))



            group_index = group_index + 1    





        # plot Test_FR(including MicSealFR plot)

        group_index = 1

        for group in groups:

            for test_seal in self.config["Tests_Seal"]:

                if test_seal['Project'] != self.project_name:

                    continue

                serial_numbers = group["SerialNumbers"]

                self.data_Group_Seal = self.df_FACT[self.df_FACT['SerialNumber'].isin(serial_numbers)]            

                data_extract_Seal = self.data_Group_Seal[self.columns_dict[test_seal["ID"]]].astype(np.float)

                data_extract_Seal['Station ID'] = self.data_Group_Seal['Station ID']

                data_extract_Seal = data_extract_Seal.groupby(["Station ID"]).mean()

                data_extract_Seal.columns = map(int, self.FR_headers(data_extract_Seal.columns))

                data_extract_Seal = data_extract_Seal.sort_index(axis=1)

                fig = plt.figure(figsize=(16, 9))

                ax = plt.gca()

                loc = plticker.MultipleLocator(base=1.0)

                ax.xaxis.set_major_locator(loc)

                plt.grid()

                tmp = pd.DataFrame(test_seal["Limits"])

                tmp.index = tmp.iloc[:, 0]

                tmp = tmp.iloc[:, 1:]

                tmp.columns = ['MIN', 'MAX']

                tmp.plot(ax=ax, logx=True)

                all_mean = data_extract_Seal.mean()

            # all_mean.index=['Overall Mean']

                all_mean.plot(ax=ax, logx=True, linestyle='--', linewidth=3.0, sharex=True)

                data_extract_Seal.T.plot(ax=ax, logx=True)

                ax.set_xlabel(test_seal["ID"] + ' Freq (Hz)', fontsize=20)

                ax.grid('on', which='both', axis='both')

                title = self.station + '_Group'+str(group_index)+ '_' + test_seal["ID"]

                filename = '%s' % self.project_name + '_' + title + '.pdf'

                plt.suptitle(title, fontsize=30)

            # ax.legend(shadow=True, fontsize=12)

                plt.savefig(os.path.join(self.work_dir, filename), dpi=200)

                pp.savefig()

                logging.info('%s Group %s  %s Plot Generation' % (self.station, group_index, test_seal["ID"]))                

            group_index = group_index + 1 

        pp.close()



    def Zip_File(self):

        zip_filename=shutil.make_archive(os.path.join(self.base_dir, self.project_name+'-'+self.station+'_Audit_'+datetime.datetime.now().strftime('%b-%d-%Y')), 'zip', self.work_dir)

        logging.info('%s.zip file generated.' %self.station)



    def copy_raw(self,filename):

        shutil.copy(filename, self.work_dir)

        logging.info('RawData file copyed.')





import sys



if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    test = FACT_AuditTool()

    test.load_global_config()

    test.load(os.path.realpath(sys.argv[1]))

    test.copy_raw(os.path.realpath(sys.argv[1]))

    test.output_FACT_rawdata()

    test.Zip_File()

    # test.output_file()

    #    test.output_figures()

    # test.Zip_File()

    logging.info('Done!')

