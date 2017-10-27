# from datetime import datetime
# created_time=datetime(2017, 7, 31, 18, 10, 10)
# user='a'
# beforuser='a'
# flag = 0
# while True:
#     if user == beforuser:
#         created_time = created_time
#     else:
#         if flag != 1:
#             now = datetime.now()
#             created_time = now
#             flag = 1
#         else:
#             created_time = now
#     print datetime.now()-created_time

cc=[{'a':1},{'b':2},{'c':3}]
print cc[::-1][0]