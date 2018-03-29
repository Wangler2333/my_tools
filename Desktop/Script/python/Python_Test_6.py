#!/usr/bin.python

import os
path='/Users/sasenyzhou'

fns=[os.path.join(root,fn) for root,dirs,files in os.walk(path) for fn in files]
for f in fns:
    if os.path.isfile(f):
       if '.txt' in f:
          print (f)
          print os.path.basename(f)
print(len(fns))



#with open('/Users/sasenyzhou/Desktop/123/12.csv') as f:
#    reader = csv.reader(f)
#   hea=der_row = next(reader)
#    highs = []
#    for row in reader:
#        highs.append(row[1])
