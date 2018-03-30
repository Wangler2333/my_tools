#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2018/3/3上午9:43
# @Author   : Saseny Zhou
# @Site     : 
# @File     : history.py
# @Software : PyCharm



history_info = """
0.0.5 -

     1. Changed task fail retry times to once.
        - running.py update
          add bool check request retry true or false
          add task return code is 6 and retied then continue next 
          code:
              /*
                  if states_code == 6 and j[1]["retry"] is False:
                        running_list.remove(j)
                        continue  
              */             
     2. Add append function for current date for summary.
        - summary_data.py update
          disable "os.system("rm -rf %s" % str(i[1]))  # 读取文件之后删除excel文件"
          disable when read finished excel then delete it
          add history summary file read and set list for delete duplicate value
          add py file check_history_summary.py for history file check
          code:  <from functions.check_history_summary import *>
              /*
                  tmp_dict = current_summary_check()
                  if tmp_dict is not False:
                     if tmp_dict.get(product, False) is not False:
                     dictInfo.extend(tmp_dict[product])
                  file_list = [x for x in set(dictInfo)]  
              */    
     3. Add change history file - <Resources/history.txt>
     4. double list set function      
     5. Add First Request Times to three times  
     
0.0.6 -
    
     1. running.py  row<241>
              running_list.append(tmp_1)     # re-request
              running_list.extend(list(tmp_1.items()))      # 20180309 17:12 modified    
"""