from bs4 import BeautifulSoup
import lxml
import re
import os,sys

station_list = {
    'station_list': ['PRO COS1', 'INCOMING COSMETIC',
                     'PRE-SWDL', 'Xenon USB Legacy',
                     'Palladium NativeDP', 'Palladium TBT',
                     'ADA BOX (AUDIO)', 'TRACKPAD FORCE CAL',
                     'TRACKPAD ACTUATOR CAL', 'FACT',
                     'BUTTON-TEST', 'SF-Info', 'WiFi BT OTA',
                     'COEX', 'PRE-BURN', 'NAND Test', 'SW-DOWNLOAD',
                     'Display RGBW (Color Test + WP Match)',
                     'FLICKER', 'Display Uniformity (LL + CU)',
                     'FOS', 'GRAPE-TEST', 'POSTBURN', 'SHIPPING-SETTINGS'
                                                      'Impedance Test', 'COSMETIC']
}

url_1 = os.path.dirname(sys.argv[0]) + '/C02TM2LQHV2L.html'
url_2 = os.path.dirname(sys.argv[0]) + '/C02VJ91YHV2L.html'

html = BeautifulSoup(open(url_2), "lxml")

#print(html.prettify())

# for i in html.find_all('tr'):
#     a = i.find_all(text='OVERRIDE')
#     if len(a) > 0:
#         print(i.td)

#
# count = 0
# for i in html.find_all('tr'):
#     count += 1
#     #if count >= 181:       # 11   / 13 <Product Header> / 181 <start>
#     a = re.findall(r'QSMC',str(i.text))
#     if len(a) > 0:
#         print(i.text)

# print(html.find_all('table',border="1")[-1].text)
#
# a = re.findall(r'PASS',html.find_all('table',border="1")[-1].text)
# print(a)
a = '[A-Z]\d-\d[A-Z]{2}-[A-Z]\d{2}'
tb = re.compile(a)

list = []

for i in html.find_all('table',border="1"):
    a = tb.findall(i.text)
    if a:
        for cell in i.findAll(re.compile("td|h")):
            list.append(str(cell.text).replace('\n','').replace(' ',''))


for j in list:
    print(j)
