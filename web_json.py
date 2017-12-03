#!/usr/bin/evn python3
#coding=utf-8
# www.iplaypy.com
 
# 针对web端json协议的通信库，通信协议为json,传出的data为json格式，接收的数据也是json格式
# 外界调用时可先初始化web_json类，如下所示：
# get调用
# web = web_json("http://baidu.com/")
# params = "abcd/select/100000?userID=1234&groupID=79"
# web.url_get(params)
# 
# post调用
# web = web_json("http://baidu.com/")
# params = "abcd/select/100000"
# data = '{"name": "jack", "id": "1"}'
# web.url_post(params, data)
 
from urllib.request import urlopen
from urllib.parse import quote
import json
 
class web_json:
    def __init__(self, base_url):
        self.base_url = base_url
         
    def get_url_data(self, params, data):
        web = urlopen(self.base_url + params, data)
        print (web.url)
        print ("status: " , web.status)
        rawtext = web.read()
        jsonStr = json.loads(rawtext.decode('utf8'))   
        print (json.dumps(jsonStr, sort_keys=False, ensure_ascii= False, indent=2))
        return jsonStr       
     
    # get方法
    def url_get(self, params):
        return self.get_url_data(params, None)
     
    # post方法
    def url_post(self, params, data):
        data=bytes(data, 'utf8')
        return self.get_url_data(params, data)

web = web_json("http://127.0.0.1:5000")
params = "/todo/api/v1.0/tasks/1"
web.url_get(params)    