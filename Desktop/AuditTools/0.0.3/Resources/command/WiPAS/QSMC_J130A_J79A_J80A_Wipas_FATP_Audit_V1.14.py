#!/usr/bin/env python2
# _*_ coding:UTF-8 _*_
# __author__ = "bobbie"

import requests
from bs4 import BeautifulSoup
import lxml
import urllib2
import urllib
import re,sys
import os,time
reload(sys)
sys.setdefaultencoding('UTF-8')

print ("\033[1;32m" + '线别格式为:F6-2FT-I16,日期格式为:08/30/2017,时间格式为:01:00' + "\033[0m"
username = 'Danny.Liu'
password = 'apple1234567890'
start_date =raw_input('请输入查询开始日期:')
Start_Time = raw_input('请输入查询开始时间:')
end_date = raw_input('请输入查询结束日期:')
End_Time = raw_input('请输入查询结束时间:')
new_date = time.strftime("%m/%d/%Y")
url = 'http://17.239.64.36/cgi-bin/WebObjects/QCR.woa/wa/logon'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36'}

def get_item():
	global html_2	
	post_data = {"UserName":username,"Password":password}
	for a in range(6):
		if a == 5:
			print ("Login QCR Error")
			os._exit(1)
		try:
			response = requests.post(url,data=post_data,headers=headers).content
		except:
			continue
		soup = BeautifulSoup(response,'lxml')
		url_1 = 'http://17.239.64.36'+soup.select('div[id="reports_links"] > a')[:-1][0]['href']
		html = requests.get(url_1,headers=headers).content
		wosid = re.findall(r'name="wosid" value="(.*?)"',html)[0]
		url_2 = 'http://17.239.64.36'+re.findall(r'<form name="criteria" method="post" action="(.*?)">',html)[0]
		break
	data_1 = {'startDateField':start_date,
			'5.1.1.3.5.1':Start_Time,
			'endDateField':end_date,
			'5.1.1.3.7.3.1':End_Time,
			'5.1.1.5':'Find Data',
			wosid:wosid}
	item = {}
	for b in range(6):
		if b == 5:
			print "Login QCR Yield Criteria Error"
			os._exit(1)
		try:	
			html_2 = requests.post(url_2,data=data_1,headers=headers).content
		except:
			continue	
		soup =BeautifulSoup(html_2,'lxml')
		content = soup.select('#e_5_1_1_11_21_7')
		reg = re.compile(r'<input checked="checked" id="ParentLine".*?type="checkbox" value="(5\.1\.1\.11\.21\.7\.1\.\w{1,2}\.1)"/>\s*?(.*?)\s*?<br/>',re.S)
		line = re.findall(reg,repr(content))
		for i in line:
			daima = i[0]
			line = i[1].replace(' ','').replace('\\n','')
			item[line] = daima
		return item
		break
def crawl(item,name):
	global html_6
	wosid_1 = re.findall(r'name="wosid" value="(.*?)"',html_2)[0]
	url_3 = 'http://17.239.64.36'+re.findall(r'<form name="criteria" method="post" action="(.*?)">',html_2)[0]
	site = re.findall(r'type="checkbox" name="Site" value="(.*?)" checked="checked" /></font>',html_2)
	ctime = str(int(float(time.time())*1000))
	new_url = 'http://17.239.64.36/cgi-bin/WebObjects/QCR.woa/'+url_3.split('/')[-4]+ '/ajax/'+url_3.split('/')[-2]+'/'+url_3.split('/')[-1]+'?'+ctime
	data_2 = '5.1.1.11.21.5.1=&_partialSenderID=5.1.1.11.21.5.1&AJAX_SUBMIT_BUTTON_NAME=5.1.1.11.21.5&_='
	for c in range(6):
		if c == 5:
			print "cancel All shift option Error"
			os._exit(1)
		try:
			html_3 = requests.post(new_url,data=data_2,headers=headers)
		except:
			continue
		break
	data_3 = {'startDateField':start_date,
			'5.1.1.3.5.1':Start_Time,
			'endDateField':end_date,
			'5.1.1.3.7.3.1':End_Time,
			'5.1.1.11.1.1.0':'0',
			'ProdType':'BTR/CTO',
			'Site':'5.1.1.11.19.3.0.1',
			item[name]:item[name],
			'5.1.1.11.21.9':'All Shifts',
			'5.1.1.11.23.0':'0',
			'5.1.1.11.29':'0',
			'5.1.1.11.31.1.0':'0',
			'Type':'FIRST',
			'5.1.1.15.1.0':'Calc Yields',
			'wosid':wosid_1}
	for d in range(6):
		if d == 5:
			print "Select line Error"
			os._exit(1)
		try:
			html_5 = requests.post(url_3,data=data_3,headers=headers).content
		except:
			continue
		soup_1 = BeautifulSoup(html_5,'lxml')
		url_4  = 'http://17.239.64.36'+ soup_1.find_all('a')[4:][1]['href']
		break
	
	for e in range(6):
		if e == 5:
			print "Get detail Stations infomations Error"
			os._exit(1)
		try:
			html_6 = requests.get(url_4).content
		except:
			continue
		with open(path + '1.html','ab') as e:
			e.write(html_6)
		break
		
def writefile(string, file):
    try:
        with open(file, 'a') as d:
            d.write(string + '\n')
    except IOError as i:
        print ('IOError:', i)

def parse():
		soup_2 = BeautifulSoup(html_6,'lxml')
		for i in soup_2.select('tr[bgcolor="#c6e7ff"]'):
			stations = ['PREBURN','ADA BOX (AUDIO)','Xenon USB Legacy','Palladium TBT','Palladium NativeDP','TRACKPAD FORCE CAL','TRACKPAD ACTUATOR CAL','RUNIN','POSTBURN']
			for m in stations:
				if m in i.text.split('\n')[6]:
					a = i.text.split('\n')[6].replace(' ','')
					b = i.text.split('\n')[10].replace(' ','')
					c = i.text.split('\n')[13].replace(' ','')
					d = i.text.split('\n')[19].replace(' ','')
					e = i.text.split('\n')[22].replace(' ','')
					f = i.text.split('\n')[26].replace(' ','')
					g = i.text.split('\n')[29].replace(' ','')
					h = i.text.split('\n')[36].replace(' ','')
					print a,b,c,d,e,f,g,h
					red = str(a)+','+ str(b)+','+ str(c)+','+ str(d)+','+ str(e)+','+ str(f)+','+ str(g)+','+ str(h)
					writefile(red,Resultpath)
			stations_2 = ['PRE-SWDL','FACT','BUTTON-TEST','SF INFO','WIFI-BT-OTA','COEX','Display RGBW (Color Test + WP Match)','FLICKER','Display Uniformity (LL + CU)','DFR FOS','GRAPE-TEST','POST-IMPEDENCE']
			for m in stations_2:
				if m in i.text.split('\n')[6]:
					a = i.text.split('\n')[6].replace(' ','')
					b = i.text.split('\n')[10].replace(' ','')
					c = i.text.split('\n')[13].replace(' ','')
					d = i.text.split('\n')[19].replace(' ','')
					e = i.text.split('\n')[22].replace(' ','')
					f = i.text.split('\n')[26].replace(' ','')
					g = i.text.split('\n')[39].replace(' ','')
					h = i.text.split('\n')[46].replace(' ','')
					print a,b,c,d,e,f,g,h
					red = str(a)+','+ str(b)+','+ str(c)+','+ str(d)+','+ str(e)+','+ str(f)+','+ str(g)+','+ str(h)
					writefile(red,Resultpath)

if __name__ == '__main__':
 	Date = time.strftime("%m/%d/%Y/%I/%M/%p")
	Resultpath = os.path.expanduser('~') +'/Desktop/' +'Retest.csv'
	if not os.path.isfile(Resultpath):
		red = "Station" + ',' + "PASS" + ',' + "FAIL" + ',' + "Total_Q'ty" + ',' + "Yield" + ',' + "Site" + ',' + "retest_Q'ty" + ',' + "retest_rate"
		writefile(red, Resultpath)
 	path = os.path.expanduser('~') + '/Desktop/'
 	q = get_item()
 	name = raw_input('请输入你要查看的线别:')
 	writefile(name +','+ start_date+'/'+Start_Time + '->' +end_date + '/'+ End_Time , Resultpath)
 	crawl(q,name)
	parse()

