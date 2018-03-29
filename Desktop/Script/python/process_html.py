

from get_pdca_info import crawl_sitemap_get
import os, sys
from bs4 import BeautifulSoup
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')

t  = crawl_sitemap_get(os.path.dirname(sys.argv[0]) + '/default.plist')
t.mkdir_logsFolder()
html = t.page_info_process('C02V614NHV2M')

#a = BeautifulSoup(html,"lxml")

#print a


'''

f = open('/Users/saseny/Downloads/2017_08_28_18_03_14/C02V614NHV2M.html','r')
html = f.readlines()
f.close()
'''

page = etree.HTML(html.upper().decode('utf-8'))
hrefs = page.xpath(u"//font")
#href2 = page.xpath(u"//b")


for i in hrefs:
   if i.text != '\0' or i.text != '\n':
        print i.text
        print i.arrlib


#for j in href2:
#    print j.text