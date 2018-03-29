#!/usr/bin/python

"""PDCA crawl, logs multithread download
"""

__author__ = "vincent jiang"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2013/08/05 21:57:19 $"
__copyright__ = "Copyright (c) 2013 vincent jiang"
__license__ = "Python"

import urllib2
import urllib
import cookielib
import os,sys
import re
import threading
import Queue
import datetime,time
import shutil
from optparse import OptionParser  
from BeautifulSoup import BeautifulSoup
import csv

MAX_THREAD_NUMBER = 10
mylock = threading.Lock()  

class MyThread(threading.Thread):
    def __init__(self,thread_name,queue_name):
        threading.Thread.__init__(self)
        self.queue = queue_name
        self.name = thread_name
        
    def run(self):
        global UNITURL
        global mydate
        global QueryByModule
        
        while True:
            mySN = self.queue.get()            
            
            #Start SN search
            #Query by Module and Query by FATP unit SN get different post data
            if re.search(r'true',QueryByModule,re.IGNORECASE):
                postdata=urllib.urlencode({
                    '7.1.3':'Search',
                    '7.1.5':mySN,
                    '7.1.7':'0',            
                })
            else:
                postdata=urllib.urlencode({
                    '7.1.1':mySN,
                    '7.1.3':'Search',
                    '7.1.7':'0',            
                })
                            
            req = urllib2.Request(
                url = UNITURL,
                data = postdata
            )
            
            #print UNITURL
            
            mylock.acquire()
            print "%s @ %s -> thread start" %(mySN,self.name)
            
            for i in range(10):
                if (i>5):
                    print "%s @ %s -> ERROR, FAIL to search find this SN on PDCA" %(mySN,self.name)
                    os._exit(1)
                try:
                    result = urllib2.urlopen(req, timeout=30).read()
                    #OK, got to process log download
                    print "%s @ %s -> query SN PDCA, attempt %s" %(mySN,self.name,i)
                    sys.stdout.flush()
                except:
                    continue
                if re.search(r'href="(.*?)">View Process Logs', result):
                    #print result
                    break
                else:
                    #Logon the PDCA again
                    logonPDCAQCR()
                    if re.search(r'true',QueryByModule,re.IGNORECASE):
                        postdata=urllib.urlencode({
                            '7.1.3':'Search',
                            '7.1.5':mySN,
                            '7.1.7':'0',            
                        })
                    else:
                        postdata=urllib.urlencode({
                            '7.1.1':mySN,
                            '7.1.3':'Search',
                            '7.1.7':'0',            
                        })
                    req = urllib2.Request(
                        url = UNITURL,
                        data = postdata
                    )
                    #print UNITURL
            
            #get UUT module SF info, sometime we do not click product moduel history  
            if (re.search(r'href="(.*?)"><img border="0".*?Open Product Module History', result)):
                match = re.search(r'href="(.*?)"><img border="0".*?Open Product Module History', result)
                tmp = match.group(1)
                myProductModuleURL = 'http://%s%s'%(PDCAIPAdress,tmp)
                moduleresult = urllib2.urlopen(myProductModuleURL, timeout=30).read()
            else:
                moduleresult = result

            try:
                getUnitModuleInfo(moduleresult)
            except:
                print "%s @ %s -> ERROR, get module info" %(mySN,self.name) 
            
            
            #print "now searching SN"
                                    
            match = re.search(r'href="(.*?)">View Process Logs', result)
            tmp = match.group(1)
            myURL = 'http://%s%s'%(PDCAIPAdress,tmp)
            
            
            
            #get log list
            result = urllib2.urlopen(myURL, timeout=30).read()
                        
            resultexist = 0
            for i in range(10):
                try:
                    result = urllib2.urlopen(myURL, timeout=30).read()
                    #print "%s->2222->%s" %(mySN,self.name)
                except:
                    continue
                if re.search(r'<a href="(.*?)" name=".*?"><img', result):
                    resultexist = 1
                    break
            
            mylock.release()            
            
            #This unit do not have processlog, thead finish
            if resultexist == 0:
                print "%s @ %s -> ERROR, do not see process log on PDCA" %(mySN,self.name)
                sys.stdout.flush()
                #self.queue.task_done()
            else:
                #Get the download link
                print "%s @ %s -> download process log from PDCA" %(mySN,self.name)
                for match in re.finditer(r'<tr>\s*?<td.*?>\s*?<font.*?>(.*?)</font>\s*?</td>\s*?<td.*?>\s*?<font.*?</font>\s*?</td>\s*?<td.*?>\s*?<font.*?<a href="(.*?)" name=".*?"><img',result):
                    # match = re.search(r'<a href="(.*?)" name=".*?"><img', result)
                    if options.regexp is not None:
                        if not re.search(options.regexp,match.group(1),re.IGNORECASE):
                            continue
                        
                    tmp = match.group(2)
                    myURL = 'http://%s%s?7,7'%(PDCAIPAdress,tmp)
                
                    for i in range(10):
                        try:
                            r = urllib2.urlopen(urllib2.Request(myURL))
                        except:
                            continue
                        if r.info().has_key('Content-Disposition'):
                            break
                    #print r.info()
                
                    if r.info().has_key('Content-Disposition'):
                        fileName = r.info()['Content-Disposition'].split('filename=')[1]
                        fileName = fileName.replace('"', '').replace("'", "")
                        #tmpdirname, tmpfilename = os.path.split(os.path.abspath(sys.argv[0]))
                        
                        if options.regexp is None:
                            with open(os.getenv("HOME")+"/Downloads/" + mydate + "/" + fileName, 'wb') as f:
                                shutil.copyfileobj(r,f)
                        else:
                            if re.search(options.regexp,fileName,re.IGNORECASE):
                                with open(os.getenv("HOME")+"/Downloads/" + mydate + "/" + fileName, 'wb') as f:
                                    shutil.copyfileobj(r,f)
                #mylock.release()
                print "%s @ %s -> thread end" %(mySN,self.name)
                sys.stdout.flush()
                #self.queue.task_done()
            self.queue.task_done()    

def logonPDCAQCR():
    #Enable cookie
    global URL
    global UNITURL
        
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    #login in to QCR first
    
    postdata=urllib.urlencode({
        'UserName':options.username,
        'Password':options.password
    })
    # 
    req = urllib2.Request(
        url = URL,
        data = postdata
    )    
    
    #try to logon PDCA first
    for i in range(10):
        if (i>5):
            print "FAIL to logon PDCA"
            os._exit(1)
        try:
            print "Logon PDCA, attempt %s"%(i)
            result = urllib2.urlopen(req, timeout=10).read()
        except:
            continue
        if re.search(r'<form name=".*?" method="post" action="(.*?)">', result):
            print "PDCA logged on"
            #get product history page URL
            match = re.search(r'<a href="(.*?)">\s*?<span id = "product_history">Product History</span>', result)
            tmp = match.group(1)
            UNITURL = 'http://%s%s'%(PDCAIPAdress,tmp)
            break
            
    #click product history, so that we can query both FATP and module
    for i in range(10):
        if (i>5):
            print "FAIL redirect to product history page"
            os._exit(1)
        try:
            print "Redirect to product history page, attempt %s"%(i)
            result = urllib2.urlopen(UNITURL, timeout=30).read()
        except:
            continue
        if re.search(r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>', result):
            print "Product history page logged on"
            
            #get the product history URL
            match = re.search(r'<form name="f_7_1" method="post" action="(.*?)">(\s|.)*?<td>SN, PS, PO, or SO:</td>', result)
            tmp = match.group(1)
            UNITURL = 'http://%s%s'%(PDCAIPAdress,tmp)
            break
    #print UNITURL
    #OK, now we have logged in QCR and let's go to systerm yield
    sys.stdout.flush()

def crawlLog():
    myqueue = Queue.Queue()
    for i in range(MAX_THREAD_NUMBER):
        mythreadname = "Thread" + str(i)
        t = MyThread(mythreadname,myqueue)
        t.setDaemon(True)
        t.start()
    # read all SN out from serialnumber.txt, and put them in the queque
    text_file = open(options.serialnumber,"r")
    lines = text_file.readlines()
    for line in lines:
        serialnumbers = line.split()
        for serialnumber in serialnumbers:
            #chomp
            if serialnumber[-1] == '\n':
                serialnumber = serialnumber[:-1]
            # print line
            myqueue.put(serialnumber)
    text_file.close()
    
    myqueue.join()

def getUnitModuleInfo(moduleresult):
    
    global Global_header
    csv_header = []
    csv_row = []
    csv_lsit = {}
    
    #print result
    soup = BeautifulSoup(moduleresult)
    
    #got unit summary data first, coming form first table for html
    table = soup.findAll('table',border="1")[0]
    fieldflag = 0
    for row in table.findAll('tr'):
        for cell in row.findAll(re.compile("td|h")):
            #if re.search(r'<form name="f_35" method="post" action="(.*?)">', result):
            if (fieldflag == 1):
                csv_row.append(cell.text)
                fieldflag = 0
            if re.search(r':$', cell.text):
                csv_header.append(cell.text)
                fieldflag = 1
            #print cell.text
    table = soup.findAll('table',border="1")[-1]
    
    '''
    Timestamp 	Station 	Serial Number 	Lot Code 	Date Code 	Info Code 	Part # 	Description 	Vendor Code
    10/11/14 2:02 AM 		DN1436605ENFQG3A2? 				655-1810D 	HDD 	SAMSUNG
    '''
    module_keys = []
    #module_keys from first row
    for cell in table.findAll('tr')[0].findAll(re.compile("td|h")):
        #print cell.text
        module_keys.append(cell.text)
    
    #ok, now we get the module list, start from 2nd row
    for row in table.findAll('tr')[1:]:
        module_list = {}
        module_values = []
        for cell in row.findAll(re.compile("td|h")):
            #print cell.text
            module_values.append(cell.text)
        for i in range(len(module_keys)):
            #print module_keys[i]
            #print module_values[i]
            module_list[module_keys[i]] = module_values[i]
    
        for i in range(len(module_keys)):
            csv_header.append('zZ %s  %s'%(module_list["Description"],module_keys[i]))
            csv_row.append(module_values[i])
    
    for i in range(len(csv_header)):
        csv_lsit[csv_header[i]] = csv_row[i]
    
    csv_header = []
    csv_row = []
        
    for key in sorted(csv_lsit.iterkeys()):
        csv_header.append(key)
        csv_row.append(csv_lsit[key])
        
    with open(os.getenv("HOME")+"/Downloads/" + mydate + "/UnitInfo_Summary.csv", 'ab') as f:
        writer = csv.writer(f)
        if (len(Global_header) < 1 or Global_header != csv_header):
            writer.writerow(csv_header)
            Global_header = csv_header
        writer.writerow(csv_row)

def parseCSV():

    #get universal header
    Universal_Header = []
    Universal_Row = []
    Universal_Value = {}

    reader = csv.reader(file(os.getenv("HOME")+"/Downloads/" + mydate + "/UnitInfo_Summary.csv", 'rb'))

    for line in reader:
        if ("Serial Number:" in line):
            for key in line:
                if not (key in Universal_Header):
                    Universal_Header.append(key)
    
    Universal_Header.sort()
    #print Universal_Header
    with open(os.getenv("HOME")+"/Downloads/" + mydate + "/UnitInfo_Summary_Sorted.csv", 'ab') as f:
        writer = csv.writer(f)
        writer.writerow(Universal_Header)
    
    MyKey = []
    MyValue = []
    MyList = {}
    
    reader = csv.reader(file(os.getenv("HOME")+"/Downloads/" + mydate + "/UnitInfo_Summary.csv", 'rb'))
    
    for line in reader:
        if ("Serial Number:" in line):
            MyKey = line
        else:
            MyValue = line
            for i in range(len(MyKey)):
                MyList[MyKey[i]] = MyValue[i]
            
            for key in Universal_Header:
                Universal_Value[key] = ''
            
            for key in sorted(MyList.iterkeys()):
                Universal_Value[key] = MyList[key]
                
            for key in Universal_Header:
                Universal_Row.append(Universal_Value[key])
            
            with open(os.getenv("HOME")+"/Downloads/" + mydate + "/UnitInfo_Summary_Sorted.csv", 'ab') as f:
                writer = csv.writer(f)
                writer.writerow(Universal_Row)
                
            Universal_Row = []
            Universal_Value = {}   


if __name__=='__main__':
    
    usage = 'usage: %prog --username=USERNAME --password=PASSWORD --serialnumber=serialnumber.txt [--regexp=regularexpression] [--pdcaurl=PDCAURL] [--querymodule=false]'  
    parser = OptionParser(usage=usage)  
    parser.add_option("--username", action="store", type="string", dest="username", help="pdca username")  
    parser.add_option("--password", action="store", type="string", dest="password", help="pdca password")
    parser.add_option("--serialnumber", action="store", type="string", dest="serialnumber", help="text file with serialnumbers")
    parser.add_option("--regexp", action="store", type="string", dest="regexp", help="regular expression for what you want to sort out of logs")
    parser.add_option("--pdcaurl", action="store", type="string", dest="pdcaurl", help="pdca URL")
    parser.add_option("--querymodule", action="store", type="string", dest="querymodule", help="query by module serialnumber instead of FATP unit serialnumber")
    (options, args) = parser.parse_args()
    
    if options.username is None or options.password is None or options.serialnumber is None :
        parser.print_help()
        sys.stdout.flush()
        os._exit(1)

    if options.querymodule is None :
        QueryByModule = 'false'
    else :
        QueryByModule = "%s"%(options.querymodule)
    
    if options.pdcaurl is None :
        PDCAIPAdress = '17.80.230.36'
    else :
        PDCAIPAdress = "%s"%(options.pdcaurl)
     
    URL = "http://%s/cgi-bin/WebObjects/QCR.woa/wa/logon"%(PDCAIPAdress)
    UNITURL = URL
    
    Global_header = []
    
    #logs will be saved here
    mydate = time.strftime("%m_%d_%Y_%I_%M_%p")
    if not os.path.exists(os.getenv("HOME")+"/Downloads/" + mydate):
        os.system('mkdir %s'%(os.getenv("HOME")+"/Downloads/" + mydate))

    st = time.time()
    
    logonPDCAQCR()
    crawlLog()
    parseCSV()
    
    print 'it takes %f sec to download'%(time.time()-st)
    print 'Logs are saved at ~/Downloads/%s'%mydate
    sys.stdout.flush()