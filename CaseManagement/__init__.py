# coding=gbk
# import csv
#
# with open("test.csv","w",encoding='utf8',newline='') as csvfile:
#  writer=csv.writer(csvfile)
#  writer.writerow(["index","a_name","b_name"])
#  for i in range(10):
#      writer.writerows([[i,str(i),str(i)]])

import xlwt                            #导入模块
wb = xlwt.Workbook(encoding = 'ascii')  #创建新的Excel（新的workbook），建议还是用ascii编码
ws = wb.add_sheet('weng')               #创建新的表单weng
ws2 = wb.add_sheet('weng1')               #创建新的表单weng
ws.write(0, 0, label = 'hello')         #在（0,0）加入hello
ws.write(0, 1, label = 'world')         #在（0,1）加入world
ws.write(1, 0, label = '你好')
wb.save('weng.xls')                    #保存为weng.xls文件



