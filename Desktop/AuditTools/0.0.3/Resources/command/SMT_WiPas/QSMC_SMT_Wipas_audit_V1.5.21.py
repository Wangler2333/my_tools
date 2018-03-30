##################################################################



#Version:1.0 2017-09-10 Wipas SMT audit Tool 

#1.5.5 Pathloss limit +/-1dB

#1.5.10 Txpower limit mean+/-0.8dB, correct header error

#1.5.11 encrypty zip file

#1.5.12 correct station name error

#1.5.16 Audit date correction

#1.5.21 Change to Insight format

##################################################################

#run script: python xxx.py xxx.csv

#input: 

#   PDCA wipas audit raw data

#output: 

#   Put stationID as column.StationID+column.TestHeadID, TestHeadID indicate slot number

#   Pathloss by line (png), relative limit (mean-station)<1dB, absolute limit 2.4G<9dB, 5G<11dB

#   Pathloss excel output, format : station name/audit results/ value

#   Pathloss overlap check, report overlapped stations, if different station fall into excatly the same pathloss, report to pdf summary report.

#   TxPower audit, limit target +/-0.8dB , tagert= mean(upperlimit,lowerlimit)

#   Summary report excel format: line, stationID+TestID, TxPower : pass/fail, pathloss Pass/fail, audit date, overdue date

#   

########################################################################

import pandas as pd

import numpy as np

from colorama import Fore,Back,Style



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

pd.options.mode.chained_assignment = None

class SMT_AuditTool:





    def __init__(self):

        pass





    def has_limit(self,col):

        return not np.isnan(np.float(self.source.ix[4, col])) and not np.isnan(np.float(self.source.ix[5, col]))





    def get_channel_type(self,column):

        col = column.lower()

        if 'tc=Pathloss:'.lower() in col and 'subtc=antenna'.lower() in col:

            return 'pathloss'

        if self.SMT_station=='WIFI-BT-COND-B':

            if 'tc=TxPower'.lower() in col and 'ant=012'.lower() in col and self.has_limit(column):

                return 'txpower'

        else:

            if 'tc=TxPower'.lower() in col and self.has_limit(column):

                return 'txpower'

    def ignore_cell_over_limit(self):

        pass





    #import orginial csv data, extract key words

    def load(self,filename):

        work_dir, short_filename = os.path.split(filename)

        self.base_dir=work_dir

        short_filename_without_ext, ext = os.path.splitext(short_filename)

        self.work_dir = os.path.join(work_dir, short_filename_without_ext)

        if not os.path.exists(self.work_dir):

            os.makedirs(self.work_dir)

        logging.info('Loading file.')

        # read orginal file, convert str to lower letter

        if 'xls' in ext.lower():

            self.source = pd.read_excel(filename, header=None)

        if 'csv' in ext.lower():

            #self.source = pd.read_csv(filename, header=None, dtype=np.str)

            first_row = pd.read_csv(filename,header=None,nrows=1)

            other_rows = pd.read_csv(filename, header=1, dtype=np.str)

            first_row.columns = other_rows.columns[0:len(first_row.columns)]

            s=pd.Series(first_row.iloc[0],index=other_rows.columns)

            self.source = pd.DataFrame(columns=other_rows.columns)

            self.source = self.source.append(s,ignore_index=True)

            s=pd.Series(self.source.columns,index=other_rows.columns)

            self.source=self.source.append(s,ignore_index=True)

            self.source=self.source.append(other_rows,ignore_index=True)

 

        logging.info('File Loaded.')

        # read .csv file

        self.version = self.source.iloc[0, 1]

        self.SMT_station=self.source.iloc[0,0]

        self.auditoverlay=self.source.iloc[0,1]

        self.site=self.source.iloc[7,0]

        self.project_name = self.source.iloc[7, 1]

        self.source.columns = self.source.iloc[1,:]





        self.txpower_columns = []

        self.pathloss_columns = []







        for col in self.source.columns:

            if type(col) is not str:

                continue

            channel_type = self.get_channel_type(col)

            if channel_type == 'pathloss':

                self.pathloss_columns.append(col)

            if channel_type == 'txpower':

                self.txpower_columns.append(col)

        self.ignore_cell_over_limit()



        self.source.loc[7:,self.pathloss_columns] = self.source.loc[7:,self.pathloss_columns].astype(np.float)

        self.source.loc[7:,self.txpower_columns] = self.source.loc[7:,self.txpower_columns].astype(np.float)



        self.pathloss_columns_24G=[]

        self.pathloss_columns_5G = []



        for col in self.pathloss_columns:

            freq = re.search(r'subsubtc=(.*?) ',col).group(1)

            if float(freq)<5000:

                self.pathloss_columns_24G.append(col)

            else:

                self.pathloss_columns_5G.append(col)



        logging.info('Version : %s' % self.version)

        logging.info('Project : %s' % self.project_name)

        logging.info('SMT_StationName: %s' %self.SMT_station)

        logging.info('Count of txPower columns : %d' % len(self.txpower_columns))

        logging.info('Count of pathloss columns : %d' % len(self.pathloss_columns))









    def pathloss_output_file(self):

        data = self.source.iloc[7:,:]

        data.loc[:,'New Station ID'] = data['Station ID'] +'_'+ data['tc=Slot Number tech=Unit']





        SMT_data=self.source.iloc[7:,:]

        SMT_data['Line Name'] = SMT_data['Station ID'].map(lambda x: self.lineName(x))

        lineNames = SMT_data['Line Name'].drop_duplicates()

        print(lineNames)

        #print('lineName :',list(set(lineNames)))



        data.loc[:,'StartTime'] = pd.to_datetime(data['StartTime']).values

        data = data.sort_values(['StartTime'],ascending=False)



        data = data.drop_duplicates('New Station ID')



        df_pathloss_columns = ['New Station ID'] + self.pathloss_columns

        df_pathloss_output = data.loc[:,df_pathloss_columns]

        df_pathloss_output1 = data.loc[:,self.pathloss_columns]

        

        pathloss_limit = pd.DataFrame(index=['Relative_Upper_Limit:Pathloss Mean + 1dB','Relative_Lower_Limit:Pathloss Mean - 1dB'],columns=self.pathloss_columns)



        pathloss_mean = data.loc[:,self.pathloss_columns].mean()

        pathloss_limit.loc['Relative_Upper_Limit:Pathloss Mean + 1dB'] = (pathloss_mean+1).values

        pathloss_limit.loc['Relative_Lower_Limit:Pathloss Mean - 1dB'] = (pathloss_mean-1).values



        #df_pathloss_output1=df_pathloss_output1.applymap(lambda x: ((pathloss_mean+1)-x)<0 )

        #df_pathloss_output1=df_pathloss_output1.applymap(lambda x: (x-(pathloss_mean+1))) 

        audit_result= ((df_pathloss_output[self.pathloss_columns].astype(np.float)-pathloss_mean).abs()>1).any(axis=1)==False

        audit_result = audit_result.map(lambda x: 'PASS' if x else 'FAIL')



        #df_pathloss_output2=df_pathloss_output1.applymap(lambda x: x>(pathloss_mean+1))

        #df_pathloss_output3=df_pathloss_output1.applymap(lambda x: x<(pathloss_mean-1))

        #df_pathloss_output1=df_pathloss_output1.applymap(lambda x: x>(pathloss_mean+1).values and lambda x: x<(pathloss_mean-1).values)



        #audit_result= ((df_pathloss_output2.any(axis=1) == False) & (df_pathloss_output3.any(axis=1) == False)).map(lambda x: "PASS" if x else "FAIL")

        #audit_result= (df_pathloss_output1.any(axis=1) == False).map(lambda x: "PASS" if x else "FAIL")





        #df_pathloss_24G = data.loc[:,self.pathloss_columns_24G].astype(np.float)

        #df_pathloss_5G = data.loc[:,self.pathloss_columns_5G].astype(np.float)



        #df_pathloss_24G = df_pathloss_24G.applymap(lambda x : x>9)

        #df_pathloss_5G = df_pathloss_5G.applymap(lambda x : x>11)



        #audit_result= ((df_pathloss_24G.any(axis=1) == False) & (df_pathloss_5G.any(axis=1) == False)).map(lambda x: "PASS" if x else "FAIL")



        audit_result[df_pathloss_output.index.drop(df_pathloss_output.dropna().index)] = "NOVALUE"



        df_pathloss_output.insert(1,'Audit Result',audit_result)



        # df_pathloss_output['Audit Result'] = df_pathloss_output.loc[:,self.pathloss_columns].astype(np.float)>9





        writer = pd.ExcelWriter(os.path.join(self.work_dir,'%s_%s_Detailed_Audit_report.xlsx'%(self.project_name,self.SMT_station)),engine='xlsxwriter')



        sheet_name  = 'Pathloss Raw Extract'

        df_pathloss_output.to_excel(writer,sheet_name=sheet_name, index=False, header=True)



        workbook = writer.book

        worksheet = writer.sheets[sheet_name]

        red_color = workbook.add_format({'bg_color': '#FF0000'})

        green_color = workbook.add_format({'bg_color': '#00FF00'})

        rows,cols = df_pathloss_output.shape





        worksheet.conditional_format(0, 1, rows, 1,

                                         {'type': 'cell', 'criteria': '==', 'value': '"FAIL"', 'format': red_color})

        worksheet.conditional_format(0, 1, rows, 1,

                                         {'type': 'cell', 'criteria': '==', 'value': '"PASS"', 'format': green_color})



        format_num = workbook.add_format()

        format_num.set_num_format('0.00')

        # worksheet.conditional_format(6,3,rows,cols,{'type':'cell','format':format1})

        worksheet.set_column(2, cols, None, format_num)







        #pathloss_limit = pd.DataFrame(index=['Upper Limit'],columns=self.pathloss_columns)

        #pathloss_limit = pd.DataFrame(index=['Upper Limit','Relative_Upper_Limit:Pathloss Mean + 1dB','Relative_Lower_Limit:Pathloss Mean - 1dB'],columns=self.pathloss_columns)

        





        #for col in self.pathloss_columns:

            #if col in self.pathloss_columns_24G:

                #pathloss_limit.loc['Upper Limit',col]=9

            #else:

                #pathloss_limit.loc['Upper Limit',col]=11









        df_pathloss_output2 = data.loc[:,df_pathloss_columns]

   

        df_pathloss_output2 = df_pathloss_output2[df_pathloss_output.loc[:,self.pathloss_columns].duplicated(keep=False)]

        #df_pathloss_output2 = df_pathloss_output2.sort_values([self.pathloss_columns[0]])

        df_pathloss_output2 = df_pathloss_output2.sort_values([self.pathloss_columns[0]]).dropna()

        sheet_name  = 'pathloss_Duplicated_Check'

        df_pathloss_output2.to_excel(writer,sheet_name=sheet_name, index=False, header=True)









        #writer.save()



        limit = self.source.ix[4:5,self.txpower_columns].astype(np.float)

        mean = limit.mean()

        limit.iloc[0,:] = mean-1.5

        limit.iloc[1,:] = mean+1.5



 

        

        data = self.source.iloc[7:,:]

        data.loc[:,'New Station ID'] = data['Station ID'] +'_'+ data['tc=Slot Number tech=Unit']

        data.loc[:,'StartTime'] = pd.to_datetime(data['StartTime']).values

        data = data.sort_values(['StartTime'],ascending=False)

        data = data.drop_duplicates('New Station ID')  





        df_txpower_columns = ['New Station ID'] + self.txpower_columns

        df_txpower_output = data.loc[:,df_txpower_columns]

        df_txpower_output['StartTime']=data['StartTime']

        Txpower_mean=df_txpower_output[self.txpower_columns].mean()

        #audit_result= ((df_txpower_output[self.txpower_columns].astype(np.float)-limit.mean.abs()>0.8).any(axis=1)==False

        audit_result= ((df_txpower_output[self.txpower_columns].astype(np.float)-Txpower_mean).abs()>0.8).any(axis=1)==False

        audit_result = audit_result.map(lambda x: 'PASS' if x else 'FAIL')



        audit_result[df_txpower_output.index.drop(df_txpower_output.dropna().index)] = "NOVALUE"

  



        Audit_lower_limit=Txpower_mean-0.8

        limit=limit.append(Audit_lower_limit,ignore_index=True)   

        Audit_Upper_limit=Txpower_mean+0.8

        limit=limit.append(Audit_Upper_limit,ignore_index=True)



        df_txpower_output.insert(1,'Audit Result',audit_result)

        #writer = pd.ExcelWriter(os.path.join(self.work_dir,'%s_Wipas_TxPower_Audit_report.xlsx'%self.project_name),engine='xlsxwriter')

        sheet_name  = 'Audit_TxPower_output'



        df_txpower_output.to_excel(writer,sheet_name=sheet_name, index=False, header=True)







        workbook = writer.book

        worksheet = writer.sheets[sheet_name]

        red_color = workbook.add_format({'bg_color': '#FF0000'})

        green_color = workbook.add_format({'bg_color': '#00FF00'})

        rows,cols = df_txpower_output.shape





        worksheet.conditional_format(0, 1, rows, 1,

                                         {'type': 'cell', 'criteria': '==', 'value': '"FAIL"', 'format': red_color})

        worksheet.conditional_format(0, 1, rows, 1,

                                         {'type': 'cell', 'criteria': '==', 'value': '"PASS"', 'format': green_color})



        format_num = workbook.add_format()

        format_num.set_num_format('0.00')

        worksheet.set_column(2, cols, None, format_num)

        writer.save()

        logging.info('Xls file saved.')

        

        #audit_time = df_txpower_output['StartTime'].iloc[0]

        audit_time = df_txpower_output['StartTime']



        deadline = audit_time+ datetime.timedelta(days=7)

        

        df_summary_output = df_txpower_output[['New Station ID','Audit Result']]

        df_summary_output.columns = ['New Station ID','TxPower Audit Result']

        df_summary_output.loc[:,'Pathloss Audit Result'] = df_pathloss_output['Audit Result']

        df_summary_output.loc[:,'Audit Overal Result']=(df_summary_output.loc[:,'TxPower Audit Result']=='PASS').mul(df_summary_output.loc[:,'Pathloss Audit Result']=='PASS').map(lambda x:'PASS' if x else 'FAIL')





        #df_summary_output.loc[:,'Audit Date'] =pd.to_datetime(df_txpower_output['StartTime']).values.strftime('%m-%d-%Y')

        #df_summary_output.loc[:,'Audit Date'] =df_txpower_output['StartTime'].strftime('%m-%d-%Y')

        #df_summary_output.loc[:,'Audit Date'] =df_txpower_output['StartTime'].values

        #df_summary_output.loc[:,'Audit Date'] =audit_time.strftime('%m-%d-%Y')

        df_summary_output.loc[:,'Audit Date'] =audit_time.map(lambda x:x.strftime('%d/%m/%Y'))



        #df_summary_output.loc[:,'Audit Date'] =audit_time.strftime('%m-%d-%Y')

        #df_summary_output.loc[:,'Effective deadline'] =datetime.datetime.now().strftime('%m-%d-%Y')

        df_summary_output.loc[:,'Effective deadline'] = deadline.map(lambda x:x.strftime('%d/%m/%Y'))



        #df_summary_output.loc[:,'Effective deadline'] = deadline.strftime('%m-%d-%Y')





        df_summary_output.insert(0,'Line Name',df_summary_output['New Station ID'].map(lambda x: self.lineName(x)))

        df_summary_output = df_summary_output.groupby(by=['Line Name','New Station ID']).sum()









        ######################################################################################################################################################################

        #Calculation for summary report (Audit Chamber QTY, Audit Pass/Fail %)

        pass_QTY=[]

        fail_QTY=[]

        Result_Columns=df_summary_output['Audit Overal Result']

        QTY_Chamber=len(Result_Columns)

        print(QTY_Chamber)

        for result in Result_Columns:

            if result=='PASS':

                pass_QTY.append(result)

            if result=='FAIL':

                fail_QTY.append(result)



        Overdue_QTY=[]

        Within_Deadline_QTY=[]

        current_time=datetime.datetime.now().strftime('%d/%m/%Y')

        deadlines=df_summary_output['Effective deadline']

        for deadline in deadlines:

            d1=datetime.datetime.strptime(current_time, "%d/%m/%Y")

            d2=datetime.datetime.strptime(deadline, "%d/%m/%Y")     

            delta=d1-d2

            print(d1,current_time)

            print(d2,deadline)

            print(delta)

            #if current_time<=deadline:

            if d1<=d2:

                Within_Deadline_QTY.append(deadline)

            #if current_time>deadline:

            if d1>d2:

                Overdue_QTY.append(deadline)





        #################################################################################################################################################

        #Output audit summary report in excel format

        writer = pd.ExcelWriter(os.path.join(self.work_dir, '%s_%s_FATP_Weekly_Audit_Summary_Report_%s.xlsx' %(self.project_name,self.SMT_station,datetime.datetime.now(

        ).strftime('%b-%d-%Y'))), engine='xlsxwriter')

        sheet_name = 'Sheet1'

        df_header = pd.DataFrame()

        s = pd.Series(['General INFO'])

        df_header=df_header.append(s,ignore_index=True)

        s = pd.Series(['Staion Name:',self.SMT_station,' ']+['Audit Overlay:',self.auditoverlay,' ']+['Audit LineName:',list(set(lineNames))])

        df_header=df_header.append(s,ignore_index=True)



        s = pd.Series([''])

        df_header=df_header.append(s,ignore_index=True)  

        s = pd.Series(['Audit Status'])

        df_header=df_header.append(s,ignore_index=True)

        s=pd.Series(['Audit Station QTY:',QTY_Chamber])

        df_header=df_header.append(s,ignore_index=True)

        s=pd.Series(['Audit Pass Station QTY:',len(pass_QTY),' ']+['Audit Fail Station QTY:',len(fail_QTY)])

        df_header=df_header.append(s,ignore_index=True)        

        s=pd.Series(['Within Deadline QTY:',len(Within_Deadline_QTY),' ']+['Overdue QTY:',len(Overdue_QTY)])

        df_header=df_header.append(s,ignore_index=True)            



        s = pd.Series([''])

        df_header=df_header.append(s,ignore_index=True) 

        df_header.to_excel(writer, sheet_name=sheet_name,index=False,header=False)

        df_summary_output.to_excel(writer,sheet_name=sheet_name,startrow=8,index=True,header=True)

        rows,cols = df_summary_output.shape





        workbook = writer.book

        worksheet = writer.sheets[sheet_name]

        green_color = workbook.add_format({'bg_color': '#00FF00'})



        red_color = workbook.add_format({'bg_color': '#FF0000'})

        format1 = workbook.add_format()

        format1.set_num_format('0.00')

        worksheet.conditional_format('C10:E200',{'type': 'text', 'criteria': 'begins with', 'value': 'Pass', 'format': green_color})

        worksheet.conditional_format('C10:E200',{'type': 'text', 'criteria': 'begins with', 'value': 'Fail', 'format': red_color})

        worksheet.conditional_format('J10:J200',{'type': 'text', 'criteria': 'begins with', 'value': 'Audit_WithinDeadline', 'format': green_color})

        worksheet.conditional_format('J10:J200',{'type': 'text', 'criteria': 'begins with', 'value': 'Audit_OverDue', 'format': red_color})

        writer.save()







        #################################################################################################################################################

        #Plot pathloss and Txpower audit results

        pp = PdfPages(os.path.join(self.work_dir, '%s_%s_Wipas_Audit_Report_%s.pdf '%(self.project_name,self.SMT_station,datetime.datetime.now(

        ).strftime('%b-%d-%Y'))))

        fig = plt.figure(figsize=(16, 9))

        plt.axis('off')

        plt.text(0.2, 0.7, self.project_name +' '+self.SMT_station+' Wipas Audit Report', fontsize=30)

        plt.text(0.4, 0.5, datetime.datetime.now(

        ).strftime('%b-%d-%Y'), fontsize=20)



        pp.savefig()



        logging.info('Generating pathloss audit report.')



        df_pathloss_output = data.loc[:,df_pathloss_columns].dropna()

        df_pathloss_output.loc[:,'Line Name'] = df_pathloss_output['New Station ID'].map(lambda x: self.lineName(x))



        for lineName in df_pathloss_output['Line Name'].drop_duplicates().values:



            tmp = df_pathloss_output[df_pathloss_output['Line Name'] == lineName]

            QTY_Chamber=len(df_pathloss_output[df_pathloss_output['Line Name'] == lineName])

            tmp.index = tmp['New Station ID']

            tmp=tmp[self.pathloss_columns]

            tmp.columns = self.simplify_Pathloss_headers(tmp.columns)

            fig = plt.figure(figsize=(16, 9))

            ax = plt.gca()

            loc = plticker.MultipleLocator(base=1.0)

            ax.xaxis.set_major_locator(loc)

            ax.set_title('%s: %s Pathloss values(dB) Audit Slots QTY: %s' %(lineName, self.SMT_station,QTY_Chamber))

            #plt.ylim(7, 12)

            tmp.astype(np.float).T.plot(ax=ax)



            #pathloss_limit.index = ['Upper Limit']

            pathloss_limit.columns = tmp.columns

            pathloss_limit.T.plot(ax=ax,linestyle='--',linewidth=3.0,sharex=True)





            x = range(len(tmp.columns))

            plt.grid()



            for label in ax.get_xmajorticklabels():

                label.set_rotation(90)

                label.set_fontsize(5) 



                label.set_horizontalalignment("right")



            ax.legend(shadow=True, fontsize=3)

            plt.savefig(os.path.join(self.work_dir, '%s_%s_%s_pathloss_values.pdf' % (self.project_name,lineName,self.SMT_station)))



            pp.savefig()

            plt.close('all')

            logging.info('%s:pathloss values generated' % lineName)





        logging.info('Generating pathloss audit report.')



        df_txpower_output = data.loc[:,df_txpower_columns].dropna()

        df_txpower_output.loc[:,'Line Name'] = df_txpower_output['New Station ID'].map(lambda x: self.lineName(x))



        for lineName in df_txpower_output['Line Name'].drop_duplicates().values:



            tmp = df_txpower_output[df_txpower_output['Line Name'] == lineName]

            QTY_Chamber=len(df_txpower_output[df_txpower_output['Line Name'] == lineName])

            tmp.index = tmp['New Station ID']

            tmp=tmp[self.txpower_columns]



            # tmp = pd.concat([tmp,limit])

            tmp.columns = self.simplify_TxPower_headers(tmp.columns)



            fig = plt.figure(figsize=(16, 9))

            ax = plt.gca()

            loc = plticker.MultipleLocator(base=1.0)

            ax.xaxis.set_major_locator(loc)

            ax.set_title('%s: %s Txpower values(dBm), Audit Slots QTY: %s' %(lineName,self.SMT_station,QTY_Chamber))

            # plt.ylim(-1, 1)

            tmp.astype(np.float).T.plot(ax=ax)



            limit.index = ['Lower Normal Test Limit : Target-1.5dB','Upper Normal Test Limit : Target+1.5dB','Lower Audit Limit : Mean-0.8dB','Upper Audit Limit : Mean+0.8dB']

            limit.columns = tmp.columns

            limit.T.plot(ax=ax,linestyle='--',linewidth=3.0,sharex=True)





            x = range(len(tmp.columns))

            plt.grid()



            for label in ax.get_xmajorticklabels():

                label.set_rotation(90)

                label.set_fontsize(6) 



                label.set_horizontalalignment("right")



            ax.legend(shadow=True, fontsize=3)

            plt.savefig(os.path.join(self.work_dir, '%s_%s_%s_Txpower_values Audit.pdf' % (self.project_name,lineName,self.SMT_station)))



            pp.savefig()

            plt.close('all')

            logging.info('%s:txpower values generated' % lineName)





        pp.close()

        

    #define how to check pathloss of different station are duplicated.

    def pathloss_Overlap(self,):

        pass



    #output Txpower audit results

    def Txpower_output_file(self):

        pass

    def lineName(self,stationName):

        if re.search(r'-([A-Z]+[0-9]+)_',stationName) != None :

            return re.search(r'-([A-Z]+[0-9]+)_',stationName).group(1)

        else:

            print('Station ignored %s :', stationName)

   

    #define Txpower headers (ant+rate+channel)   

    def simplify_TxPower_headers(self, headers):

        new_Txpower_headers = []

        for header in headers:

            #print (header)

            #ant = re.search(r'ant=(\d)', header).group(1) or re.search(r'stream=(\d)',header).group(1)



            if re.search(r'stream=(\d)', header) != None:

                ant=re.search(r'stream=(\d)', header).group(1)

            else:

                ant=re.search(r'ant=(\d):',header).group(1)

            channel = re.search(r'freq=(\d+)', header).group(1)

            rate=re.search(r'rate=(.+?):',header).group(1)



            new_Txpower_headers.append('ANT'+ant+"/" +channel+ "/" + rate)

        return new_Txpower_headers



  #define pathloss headers (ant+rate+channel)   

    def simplify_Pathloss_headers(self, headers):

        new_Pathloss_headers = []

        for header in headers:

            ant = re.search(r'ant=(\d)', header).group(1) 

            channel = re.search(r'subsubtc=(\d+)', header).group(1)

            new_Pathloss_headers.append('ANT'+ant+ "/" +channel)

        return new_Pathloss_headers







    def Zip_File(self):

        zip_filename=shutil.make_archive(os.path.join(self.base_dir, self.project_name+'-'+self.SMT_station+'_Wipas_Audit_'+datetime.datetime.now().strftime('%b-%d-%Y')), 'zip', self.work_dir)

        #zip_filename = os.path.join(self.base_dir, self.project_name+'_Wipas_Audit_'+datetime.datetime.now().strftime('%b-%d-%Y'))+".zip"

        #zip_filename.setpassword('111')

        #os.system("zip -P work_dir %s -r %s"%(zip_filename,self.work_dir))

        #os.system("zip -P password %s -r %s"%(zip_filename))

        logging.info('TxWipas Audit.zip file generated.')

        

        

    def copy_raw(self,filename):

        shutil.copy(filename, self.work_dir)

        logging.info('Audit RawData file copyed.')



import sys

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO,format = '%(asctime)s - %(levelname)s: %(message)s')

    test = SMT_AuditTool()

    test.load(os.path.realpath(sys.argv[1]))

    test.copy_raw(os.path.realpath(sys.argv[1]))

    test.pathloss_output_file()



    test.Zip_File()

    logging.info('Done!')

