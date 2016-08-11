#coding=utf-8
'''

@author: ldl

'''

###
###  update 20160801
###     A0       B1         C2         D3       E4      F5        G6          H7       I8       J9
###  接口地址    endpoint    method    headers    json    code    scene_desc    exec    result     pass

###  update 20160811
###   0        1         2          3         4       5       6          7             8            9         10         11
### 接口地址    endpoint    method    headers    json    data    params    checkpoint    scene_desc    exec    resp_body    pass

import os
import requests
import xlrd
import json

from xlutils.copy import copy
from sys import argv



ls = os.linesep
sep_o = os.path.sep
testcase=''

if len(argv) == 1:

    testcase = 'test20160811_nono.xls'
elif len(argv) == 2:
    testcase = argv[1]
print testcase

def doTest():
    data = xlrd.open_workbook(testcase)
    table = data.sheet_by_index(0)
    write_data = copy(data) 
    for row in range(1,table.nrows):
        callAPI(write_data,row,tuple(table.row_values(row)))   
    write_data.save(testcase) 

def callAPI(write_data,row,params):
    if params[9] == 'yes':
        resp =''
        resp_json=''
        resp_text=''
#         print params
        if params[2] == "POST":
            if params[4]:
                resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),json=eval(params[4]))        
               
            elif params[5]:
                resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),data=eval(params[5]))        
#                 print row,"RESP::",resp.text
        elif params[2] == "GET":
            resp = requests.request(params[2],params[0]+params[1],headers=eval(params[3]),params=eval(params[6]))        
#             print row,"RESP::",resp.text            
        print row,"RESP::",resp.text
        try:
            resp_json = resp.json()
            json_string = json.dumps(resp_json,indent=4,ensure_ascii=False)
            if len(json_string)> 32737:
                json_string=u'响应值过大，请参看日志记录'
            write_data.get_sheet(0).write(row,10,json_string)  
        except ValueError:
            resp_text = resp.text
            write_data.get_sheet(0).write(row,10,resp_text)  
 
        pass_res = "FAIL"        
        if isinstance(resp_json,dict):            
            pass_num = 0             
            check_point_dict = eval(params[7])
            for i in check_point_dict:
                if resp_json.get(i,None) == check_point_dict[i]:
                    pass_num += 1
            check_point_dict_length = len(check_point_dict)
            if pass_num == check_point_dict_length:
                pass_res = 'PASS'
                print u"####通过的checkpoint数为%s，checkpoint总数为：%s！####" % (pass_num,check_point_dict_length)
        write_data.get_sheet(0).write(row,11,pass_res)           


if __name__ == "__main__":
    doTest()
        
        
        
    
    


