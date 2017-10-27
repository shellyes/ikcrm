#coding:utf-8
import time
from datetime import datetime

#当前时间
time_now = time.localtime()

datetime_now = datetime.now()

#直接生成datetime类型
a = datetime(2017, 8, 1, 0, 0, 0)
b = datetime(2017, 11, 7, 18, 34, 41)
#字符串转化为datetime类型
revisit_time = '2018-08-30 14:31:30'
created_time = '2018-08-30 14:38:30'
revisit_time = datetime.strptime(revisit_time, '%Y-%m-%d %H:%M:%S')
created_time = datetime.strptime(created_time, '%Y-%m-%d %H:%M:%S')



print '获取datetime的年月日',a.year, a.month, a.day
print '获取localtime的年月日',time_now.tm_year,time_now.tm_mon,time_now.tm_mday

time_a_b = b-a
time_revisit_created = revisit_time-created_time
print (datetime_now-a).days>=0
print time_revisit_created.days == -1

start_time = datetime(2017, 7, 1, 0, 0, 0)
now_time = datetime.now()
print (start_time-now_time ).days >=0



