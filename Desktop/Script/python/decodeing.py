
import base64


file = '/Users/saseny/Desktop/123.log'
file_out = '/Users/saseny/Desktop/1234.log'

f = open(file,'r')
f_obj = f.readlines()
f.close()

for i in f_obj:
    a = base64.decodestring(i)
    with open(file_out,'a') as d:
        d.write(a)
    print a