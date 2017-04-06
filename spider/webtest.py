# -*- coding: utf-8 -*  
import os   #Python的标准库中的os模块包含普遍的操作系统功能  
import re   #引入正则表达式对象  
import urllib   #用于对URL进行编解码  
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  #导入HTTP处理相关的模块  
from testrealmonitor import testrealmonitor
      
      

        
class ServerHTTP(BaseHTTPRequestHandler): 
    test_realmonitor=testrealmonitor() 
    def distribute(self):
        path=self.path  
        print path  

        #获取post提交的数据  
        datas = self.rfile.read(int(self.headers['content-length'])) 
        datas = urllib.unquote(datas).decode("utf-8", 'ignore')  
        print datas 
        
        switch={
                '/start_mdb':self.test_realmonitor.start_page,
                '/kill_mdb':self.test_realmonitor.kill_page,
                '/change_role':self.test_realmonitor.change_role_page,
                '/deal_mdb_data':self.test_realmonitor.deal_mdb_data
                }
        func=switch[path]
        if func:
            buf=func(path,datas) 
        else:
            buf="error "       
        self.send_response(200)  
        self.send_header("Content-type","text/html")  
        self.send_header("test","This is test!")  
        self.end_headers()  
 
        self.wfile.write(buf)        
        
    def do_GET(self): 
        path = self.path  
        #拆分url(也可根据拆分的url获取Get提交才数据),可以将不同的path和参数加载不同的html页面，或调用不同的方法返回不同的数据，来实现简单的网站或接口  
        query = urllib.splitquery(path)  
        print query          
        self.send_response(200)  
        self.send_header("Content-type","text/html")  
        self.send_header("test","This is test!")  
        self.end_headers()  
        buf = self.test_realmonitor.get_page
        self.wfile.write(buf)  
          
    def do_POST(self):  
        #获取post提交的数据  
        datas = self.rfile.read(int(self.headers['content-length'])) 
        datas = urllib.unquote(datas).decode("utf-8", 'ignore')  
        buf=self.test_realmonitor.distribute(self.path,datas)
        self.send_response(200)  
        self.send_header("Content-type","text/html")  
        self.send_header("test","This is test!")  
        self.end_headers()   
        self.wfile.write(buf)  
      
#启动服务函数  
def start_server(port):  
    http_server = HTTPServer(('', int(port)), ServerHTTP)  
    http_server.serve_forever() #设置一直监听并接收请求  
  
os.chdir('./')  #改变工作目录到 static 目录  
start_server(8000)  #启动服务，监听8000端口  