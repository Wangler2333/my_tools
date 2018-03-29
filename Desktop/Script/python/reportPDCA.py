 #!/usr/bin/env python
# _*_ coding:UTF-8 _*_
# __author__ = "bobbie"

# 1,增加线别，班别选择
# 2,可以查询一周数据,也可以查询单天数据
# 3,修复第一版数据获取不全面问题

import requests
from bs4 import BeautifulSoup
import lxml
import urllib2
import urllib
import re,sys
import os,time
#reload(sys)
#sys.setdefaultencoding('UTF-8')

#print "\033[1;32m" + '''
#输入月份查询:格式为 08
#输入开始日期:格式为 21
#可以连续查询起始日期后5天数据:(21-26)
#班别选择:N ->夜班 D ->白班
#线别添加:格式为:F6-1FT-B16,F6-1FT-C16
#选择其他或者不选查询一天数据:
#需要选择开始日期和开始时间段:开始日期和结束日期不写默认为当天 开始时间格式为：08:00 结束时间：20:00
#''' + "\033[0m"

username = 'Danny.Liu'
password = 'apple1234567890'
url = 'http://17.239.64.36/cgi-bin/WebObjects/QCR.woa/wa/logon'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36'}

def get_item():
	global html_2	
	post_data = {"UserName":username,"Password":password}
	for a in range(6):
		if a == 5:
			#print "Login QCR Error"
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
			#print "Login QCR Yield Criteria Error"
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
			#print "cancel All shift option Error"
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
			#print "Select line Error"
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
			#print "Get detail Stations infomations Error"
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
					if c =='':
						c = i.text.split('\n')[16].replace(' ','')
						d = i.text.split('\n')[23].replace(' ','')
						e = i.text.split('\n')[26].replace(' ','')
						f = i.text.split('\n')[30].replace(' ','')
						g = i.text.split('\n')[43].replace(' ','')
						if g =='':
							g = i.text.split('\n')[33].replace(' ','')
							h = i.text.split('\n')[40].replace(' ','')
						else:
							h = i.text.split('\n')[50].replace(' ','')
					else:
						d = i.text.split('\n')[19].replace(' ','')
						e = i.text.split('\n')[22].replace(' ','')
						f = i.text.split('\n')[26].replace(' ','')
						g = i.text.split('\n')[29].replace(' ','')
						h = i.text.split('\n')[36].replace(' ','')
					print a,b,c,d,e,f,g,h
					red = str(a)+','+ str(b)+','+ str(c)+','+ str(d)+','+ str(e)+','+ str(f)+','+ str(g)+','+ str(h)
					writefile(red,Resultpath)
			stations_2 = ['PRE-SWDL','FACT','BUTTON-TEST','WIFI-BT-OTA','COEX','Display RGBW (Color Test + WP Match)','FLICKER','Display Uniformity (LL + CU)','DFR FOS','GRAPE-TEST','POST-IMPEDENCE']
			for m in stations_2:
				if m in i.text.split('\n')[6]:
					a = i.text.split('\n')[6].replace(' ','')
					b = i.text.split('\n')[10].replace(' ','')
					c = i.text.split('\n')[13].replace(' ','')
					if c =='':
						c = i.text.split('\n')[16].replace(' ','')
						if c =='':
							c = i.text.split('\n')[16].replace(' ','')
							d = i.text.split('\n')[23].replace(' ','')
							e = i.text.split('\n')[26].replace(' ','')
							f = i.text.split('\n')[30].replace(' ','')
							g = i.text.split('\n')[33].replace(' ','')
							h = i.text.split('\n')[40].replace(' ','')
						else:
							c = i.text.split('\n')[16].replace(' ','')
							d = i.text.split('\n')[23].replace(' ','')
							e = i.text.split('\n')[26].replace(' ','')
							f = i.text.split('\n')[30].replace(' ','')
							g = i.text.split('\n')[43].replace(' ','')
							h = i.text.split('\n')[50].replace(' ','')
					else:
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
	Resultpath = os.path.expanduser('~') +'/Desktop/' + 'Retest.csv'
	if not os.path.isfile(Resultpath):
		red = "Station" + ',' + "PASS" + ',' + "FAIL" + ',' + "Total_Q'ty" + ',' + "Yield" + ',' + "Site" + ',' + "retest_Q'ty" + ',' + "retest_rate"
		writefile(red, Resultpath)
 	path = os.path.expanduser('~') + '/Desktop/'
 	week = []
	a =raw_input('请输入查询月份:')
	b =int(raw_input('请输入查询月份开始日期:'))
	shift = raw_input('请输入你想查看的班别 N or D:')
	for m in range(1,7):
		start_date = '%s/%s/2017' % (a,b)
		b+= 1
		week.append(start_date)
	i = raw_input('请输入你要添加的线别,用逗号隔开:')
	names = i.split(',')
	if i =='':
		names = ['F6-2FT-I16','F6-2FT-J16']
	for k in names:
		name = k		
		if shift == 'D':
			t = [(week[0],'08:00',week[0],'20:00'),(week[1],'08:00',week[1],'20:00'),(week[2],'08:00',week[2],'20:00'),(week[3],'08:00',week[3],'20:00'),(week[4],'08:00',week[4],'20:00')]
		elif shift == 'N':
			t = [(week[0],'20:00',week[1],'08:00'),(week[1],'20:00',week[2],'08:00'),(week[2],'20:00',week[3],'08:00'),(week[3],'20:00',week[4],'08:00'),(week[4],'20:00',week[5],'08:00')]
		else:
			start_date =raw_input('请输入查询开始日期:')
			end_date = raw_input('请输入查询结束日期:')
			Start_Time = raw_input('请输入查询开始时间:')		
			End_Time = raw_input('请输入查询结束时间:')
			new_date = time.strftime("%m/%d/%Y")
			if start_date == '' and end_date == '':
				start_date = new_date
				end_date =new_date
			t = [(start_date,Start_Time,end_date,End_Time)]
		for i in t:
			start_date = i[0]
			Start_Time = i[1]
			end_date = i[2]
			End_Time = i[3]
		 	q = get_item()
		 	writefile(name +','+start_date +'-'+shift , Resultpath)
		 	crawl(q,name)
			parse()

