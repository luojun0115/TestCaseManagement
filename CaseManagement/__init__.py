# coding=gbk
# import csv
#
# with open("test.csv","w",encoding='utf8',newline='') as csvfile:
#  writer=csv.writer(csvfile)
#  writer.writerow(["index","a_name","b_name"])
#  for i in range(10):
#      writer.writerows([[i,str(i),str(i)]])

import xlwt                            #����ģ��
wb = xlwt.Workbook(encoding = 'ascii')  #�����µ�Excel���µ�workbook�������黹����ascii����
ws = wb.add_sheet('weng')               #�����µı�weng
ws2 = wb.add_sheet('weng1')               #�����µı�weng
ws.write(0, 0, label = 'hello')         #�ڣ�0,0������hello
ws.write(0, 1, label = 'world')         #�ڣ�0,1������world
ws.write(1, 0, label = '���')
wb.save('weng.xls')                    #����Ϊweng.xls�ļ�



