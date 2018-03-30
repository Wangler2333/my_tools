#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     : 2017/12/11下午12:05
# @Author   : Saseny Zhou
# @Site     : 
# @File     : config.py
# @Software : PyCharm Community Edition


import plistlib
import os
import sys

download = {
    'app': '/Applications/Safari.app',
    'delay': 3,
    'request':
        {
            'my_location':

                {
                    'new_window': (124, 5),
                    'create': (128, 34),
                    'ip_input': (865, 37),
                    'user_input': (1694, 74),
                    'username': (964, 574),
                    'login': (1015, 680),
                    'report': (510, 73),
                    'restore report': (531, 292),
                    'default': (676, 291),
                    'download': (1433, 164)
                },

        },
    'info':
        {
            'ip': 'https://172.24.70.50/groundhog/index.php',
            'username': 'J79_TE',
            'password': 'for79gh',
            'quit delay': 20
        }
}

plistlib.writePlist(download, os.path.join(os.path.dirname(sys.argv[0]), 'config.plist'))
