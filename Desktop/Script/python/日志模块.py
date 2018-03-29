# import logging
# logging.basicConfig(filename='access.log',
#                     format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S %p',
#                     level=40)
#
#
# logging.debug('debug')
# logging.info('info')
# logging.warning('warning')
# logging.error('error')
# logging.critical('critical')



#Formater,handler,logger,filter
# import logging
# formatter1=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S %p',)
#
# fh1=logging.FileHandler('test1.log')
# fh2=logging.FileHandler('test2.log')
# fh3=logging.FileHandler('test3.log')
# ch=logging.StreamHandler()
#
# fh1.setFormatter(formatter1)
# fh2.setFormatter(formatter1)
# fh3.setFormatter(formatter1)
# ch.setFormatter(formatter1)
#
#
#
# logger1=logging.getLogger('egon')
# logger1.setLevel(10)
# logger1.addHandler(fh1)
# logger1.addHandler(fh2)
# logger1.addHandler(fh3)
# logger1.addHandler(ch)
#
# # logger1.debug('debug')
# # logger1.info('info')
# # logger1.error('error')
# # logger1.warning('warning')
# logger1.critical('critical')
















# import logging
# formatter1=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S %p',)
#
# ch=logging.StreamHandler()
# ch.setFormatter(formatter1)
# ch.setLevel(10)
#
# logger1=logging.getLogger('egon')
# logger2=logging.getLogger('egon')
# logger1.setLevel(20)
# logger2.setLevel(20)
#
# logger1.addHandler(ch)
#
# logger1.debug('debug')
# logger1.info('info')
# logger1.error('error')
# logger1.warning('warning')
# logger1.critical('critical')




import logging
import my_log_settings
my_log_settings.load_my_logging_cfg()


logger1=logging.getLogger(__name__)
logger2=logging.getLogger('collect')


logger1.debug('默认日志的debug')
logger2.debug('给老板一封信')











