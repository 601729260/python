# -*- coding: utf-8 -*  
import os   #Python的标准库中的os模块包含普遍的操作系统功能  
import re   #引入正则表达式对象  
import urllib   #用于对URL进行编解码  
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  #导入HTTP处理相关的模块  
from subprocess import Popen, PIPE
from __builtin__ import exit
      

class testrealmonitor(BaseHTTPRequestHandler):
    '''
    用于测试帐处realmonitor功能
    '''


    def __init__(self):
        self.ip='localhost'
        self.userport='15600' 
        self.rasport='57100'
        self.abmport='45021'  
        self.is_oid=0   
        self.servidindex=3
        self.acctidindex=0
        self.billidindex=2
        self.oidindex=''
        self.get_page='''<!DOCTYPE HTML> 
                <html> 
                <head><title>Get page</title></head> 
                <body> 
                 <form action="deal_mdb_data" method="post"> 
                <input type="submit" value="set_env" name=qr/ style="width:200px;height:30px">  
                ip <input type="text" value="" name=ip>
                userport <input type="text" value="" name=userport>
                abmport <input type="text" value="" name=abmport>
                rasport <input type="text" value="" name=rasport>
                is_oid <input type="text" value="" name=is_oid>
                <br/>
                <input type="submit" value="insert_CAbmMonitorQueue" name=qr/ style="width:200px;height:30px">
                insert into CAbmMonitorQueue values(63, 217032707, 0, 117032707272240, 0, 20061013031024, 103000, 4, 0, 0, 0, '');
                <br/>                 
                <input type="submit" value="prepare_mdbdata" name=qr/ style="width:200px;height:30px">
                prepare_mdbdata
                <br/>
                <input type="submit" value="select_mdbdata" name=qr/ style="width:200px;height:30px">
                query_data  
                serv_id <input type="text" value="" name=serv_id>
                acct_id <input type="text" value="" name=acct_id>
                <label><input name="for_insert" type="checkbox" value=""/>used for insert </label>
                </form>                                 
                <form action="start_mdb" method="post"> 
                <input type="submit" value="START_MDB" name=qr/ style="width:200px;height:30px">
                <label><input name="user_mdb" type="checkbox" value="" checked="checked"/>user_mdb</label> 
                <label><input name="abm_mdb" type="checkbox" value="" checked="checked"/>abm_mdb </label> 
                <label><input name="aps_mdb" type="checkbox" value="" checked="checked"/>aps_mdb </label>
                </form> 
                <form action="deal_shell_page" method="post"> 
                <input type="submit" value="check_mdb" name=qr/ style="width:200px;height:30px"> 
                  ps -ef|grep mdb_frame
                <br/>
                <input type="submit" value="abm_insert_zwq" name=qr/ style="width:200px;height:30px">
                AbmMdbTest -w SYNCBQ -i  /result/config/abm/abm_mdb_query.cfg
                src_type <input type="text" value="" name=src_type>
                <br/>                
                <input type="submit" value="abm_sync_book" name=qr/ style="width:200px;height:30px">
                AbmMdbTest -w SYNCBOOK -i  /result/config/abm/abm_mdb_query.cfg
                <br/>
                 <input type="submit" value="kill_mdb" name=qr/ style="width:200px;height:30px">
                 kill the mdb 
                 <br/>
                <input type="submit" value="load_xbuf" name=qr/ style="width:200px;height:30px">
                 load_xbuf 
                 <br/>  
                 <input type="submit" value="start_realmonitor" name=qr/ style="width:200px;height:30px">  
                 <input type="submit" value="kill_realmonitor" name=qr/ style="width:200px;height:30px">        
                </form>
                <form action="change_role" method="post"> 
                <input type="submit" value="change_role" name=qr/ style="width:200px;height:30px"> 
                <label><input name="user_mdb" type="checkbox" value="" checked="checked"/>user_mdb</label> 
                <label><input name="abm_mdb" type="checkbox" value="" checked="checked"/>abm_mdb </label> 
                <label><input name="aps_mdb" type="checkbox" value="" checked="checked"/>aps_mdb </label> 
                </form> 
                <br/>                                               
                </body> 
                </html>''' 
        
        self.return_page='''<!DOCTYPE HTML> 
        <html> 
            <head><title> page</title></head> 
            <body>%s :<br/>
                <font size=1>%s</font>  <br />
                Path:%s<br/>
                %s<br/>                
                <form action="get_page" method="get"> 
                <input type="submit" value="BACK" name=qr/>
                </form>           
            </body> 
        </html>'''
    def awk_v_str(self,instr,filtstr,pre_str,field_list,last_str):
        pattern=re.compile(r'\n')
        list1=pattern.split(instr)
        str=''
        pattern2=re.compile(r'%s'%filtstr)
        field_list.sort()
        for value in list1:  
            fieldstr='' 
            if value:
                str=str+pre_str
                loopnum=0
                value_list=pattern2.split(value)
                field_all=range(0,len(value_list))
                print field_list
                field_out=list(set(field_all).difference(set(field_list)))
                field_out.sort()
                print field_out
                for field_num in field_out:          
                    fieldstr=fieldstr+value_list[field_num]
                    loopnum=loopnum+1
                    if(loopnum<len(field_out)):
                        fieldstr=fieldstr+filtstr 
                str=str+fieldstr+last_str+'\n'
        return str    
    def grep_mdb_str(self,instr):            
            str1=self.grep_v_str(instr,"mdb_client")
            str=self.grep_v_str(str1,"Connect to mdb server")
            print str
            return str
    def grep_v_str(self,instr,filtstr):
            pattern=re.compile(r'\n')
            list=pattern.split(instr)
            str=''
            pattern=re.compile(r'%s'%filtstr)
            for value in list:                
                match=pattern.search(value)
                if match:
                    continue
                pattern2=re.compile(r'^$')
                match2=pattern2.search(value)
                if match2:
                    continue
                pattern4=re.compile(r'^ $')
                match4=pattern4.search(value)
                if match4:
                    continue
                str=str+value+'\n'
            return str
    def grep_str(self,instr,filtstr):
            pattern=re.compile(r'\n')
            list=pattern.split(instr)
            str=''
            pattern2=re.compile(r'%s'%filtstr)
            num=0
            for value in list:                         
                match=pattern2.search(value)
                if not match:
                    continue 
                str=str+value+'\n'                        
            return str
    def awk_str(self,instr,filtstr,field_list):
            pattern=re.compile(r'\n')
            list=pattern.split(instr)
            str=''
            pattern2=re.compile(r'%s'%filtstr)
            for value in list:  
                fieldstr='' 
                if value:
                    loopnum=0
                    value_list=pattern2.split(value)
                    for field_num in field_list:                
                        fieldstr=fieldstr+value_list[field_num]
                        loopnum=loopnum+1
                        if(loopnum<len(field_list)):
                            fieldstr=fieldstr+filtstr 
                    str=str+fieldstr+'\n'
            return str        
    def transfer_br(self,str):
        strout=''
        pattern=re.compile(r'\n')
        list=pattern.split(str)
        for value in list:
            strout=strout+value+'<br/>'
        return strout
    def distribute(self,path,datas): 
        print path  
        print datas 
        switch={
                '/start_mdb':self.start_page,
                '/deal_shell_page':self.deal_shell_page,
                '/change_role':self.change_role_page,
                '/deal_mdb_data':self.deal_mdb_data
                }
        func=switch[path]
        if func:
            buf=func(path,datas) 
        else:
            buf="error "   
        return buf    
    def re_is_have(self,datas,param):
        paramvalue=''
        str='&('+param+')='
        pattern=re.compile(r'%s'%str)
        list=pattern.findall(datas)
        if len(list)>0:
            paramvalue=list[0] 
        return  paramvalue
    def re_get_param(self,datas,param):
        paramvalue=''
        str=param+'=([\w.]+)'
        pattern=re.compile(r'%s'%str)
        list=pattern.findall(datas)
        if len(list)>0:
            paramvalue=list[0] 
            return  paramvalue        
    def set_env(self,datas):
        if self.re_get_param(datas,'ip'):
            self.ip=self.re_get_param(datas,'ip')     
        if self.re_get_param(datas,'abmport'):
            self.abmport=self.re_get_param(datas,'abmport') 
        if self.re_get_param(datas,'rasport'):        
            self.rasport=self.re_get_param(datas,'rasport')  
        if  self.re_get_param(datas,'userport'):         
            self.userport=self.re_get_param(datas,'userport')
        if  self.re_get_param(datas,'is_oid'):           
            self.is_oid=self.re_get_param(datas,'is_oid')  
        if  self.is_oid=='1':   
            self.servidindex=4
            self.acctidindex=1
            self.billidindex=3  
            self.oidindex=0                      
        buf=''
        return buf  
    def insert_CAbmMonitorQueue(self,datas):
        str=''
        abmproc=Popen(["mdb_client", self.ip,self.abmport], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (abmout, abmerr) = abmproc.communicate('''insert into CAbmMonitorQueue values(0, 217032707, 0, 117032707272240, 0, 20061013031024, 103000, 4, 0, 0, 0, '');
            insert into CAbmMonitorQueue values(1, 217032707, 0, 117032707272240, 0, 20061013031024, 103000, 4, 0, 0, 0, '');
            insert into CAbmMonitorQueue values(2, 217032707, 0, 117032707272240, 0, 20061013031024, 103000, 4, 0, 0, 0, '');            
            exit   
            ''')
        if abmproc.returncode != 0:
            str=str+abmerr
        else:
            str=str+abmout  
        return str      
    
    def change_role(self,mdb):
        switch={
                'abm_mdb':Popen(["mdb_change_role", self.ip,self.abmport], stdout=PIPE, stdin=PIPE, stderr=PIPE),
                'user_mdb':Popen(["mdb_change_role", self.ip,self.userport], stdout=PIPE, stdin=PIPE, stderr=PIPE),
                'aps_mdb':Popen(["mdb_change_role", self.ip,self.rasport], stdout=PIPE, stdin=PIPE, stderr=PIPE)
                }
        
        proc = switch[mdb]
        (out, err) = proc.communicate('2\n3\n')
        os.system("ps -ef|grep change_role|awk '{print $2}'|xargs kill -9")
        if proc.returncode != 0:
            return err
        else:
            return out    

    def start_usermdb(self):  
        command='mdb_frame'
        os.system('mdb_frame -i /result/config/billing40/user_mdb_start_15600.cfg>/dev/null &')
    def start_apsmdb(self):  
        command='mdb_frame'
        os.system('mdb_frame -i /result/config/aps50_ct/ras_50_mdb_57100.cfg>/dev/null &')
    def start_abmmdb(self):  
        command='mdb_frame'
        os.system('mdb_frame -i /result/config/abm/abm_45021_frame.cfg>/dev/null &')        
    
    def start_page(self,path,datas):

        print path;
        print datas;
        pattern=re.compile(r'([\w]+_mdb)')
        list=pattern.findall(datas)
        print list
        switch={
                'user_mdb':self.start_usermdb,
                'aps_mdb':self.start_apsmdb,
                'abm_mdb':self.start_abmmdb
                }
        str='';
        for mdb in list:
            print "start %s begin"%mdb
            switch[mdb]()
            str.join(mdb)
            str.join(" ")
            print "start %s end"%mdb
        os.system('ps -ef|grep mdb_frame')
        
        html_from=""
        buf = self.return_page%("start mdb ok ",str,path,html_from)        
        return buf
    
    def deal_shell_page(self,path,datas):
        print path;
        print datas;
        pattern=re.compile(r'qr/=([\w]+)')
        list=pattern.findall(datas)
        print list
        switch={
                'kill_mdb':"ps -ef|grep mdb_frame|awk '{print $2}'|xargs kill -9",
                'check_mdb':"ps -ef|grep mdb_frame",
                'load_xbuf':"loader.sh",
                'start_realmonitor':"ecframe -i /result/config/abm/realmonitor_01.xml>/dev/null &",
                'kill_realmonitor':"ps -ef|grep ecframe|awk '{print $2}'|xargs kill -9",
                'abm_insert_zwq':"AbmMdbTest -w SYNCBQ -i  /result/config/abm/abm_mdb_query.cfg",
                'abm_sync_book':"AbmMdbTest -w SYNCBOOK -i  /result/config/abm/abm_mdb_query.cfg"                
                }
        str=''
        for deal_data in list:
            print "start %s begin"%deal_data
            out=os.popen(switch[deal_data])
            strout=out.readlines()
            for line in strout:
                str=str+line+'<br/>'
            print "start %s end"%deal_data
        #修改src_type    
        src_type=0;
        if  self.re_get_param(datas,'src_type'):           
            src_type=self.re_get_param(datas,'src_type')
            abmproc=Popen(["mdb_client", self.ip,self.abmport], stdout=PIPE, stdin=PIPE, stderr=PIPE)
            (abmout, abmerr) = abmproc.communicate('''update CAbmMonitorQueue set source_type=%s where acct_id=217032707;
            exit'''%src_type)
            if abmproc.returncode != 0:
                str=str+abmerr
            else:
                str=str+self.transfer_br(self.grep_mdb_str(abmout))                          
        html_from=""
        buf = self.return_page%("exec func ok ",str,path,html_from)      
        return buf    
    def change_role_page(self,path,datas):
        print path;
        print datas;
        pattern=re.compile(r'([\w]+_mdb)')
        list=pattern.findall(datas)
        print list
        str='';
        for mdb in list:
            print "%s change role begin"%mdb
            out=self.change_role(mdb)
            print out
            str.join(mdb)
            str.join(" ")
            print "%s change role  end"%mdb  
            
        html_from=""      
        buf = self.return_page%("change role ok",str,path,html_from)                     
        return buf 
    
    def prepare_mdbdata(self,datas):
        str=''
        abmproc=Popen(["mdb_client", self.ip,self.abmport], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (abmout, abmerr) = abmproc.communicate('''delete from CAbmBook where acct_id=217032707;
            insert into CAbmBook values( 217032707, 0, 1, 99, 0, 19900101, 20301231, 0, 0, 0); 
            insert into CAbmBook values( 217032707, 317032707, 217032707, 500601, 5000, 19900101, 20670118, 0, 0, 0);
            delete from CAbmAlarmTrack where acct_id=217032707;
            insert into CAbmAlarmTrack values(217032707,317032707);
            delete from CAbmUserService where acct_id=217032707;
            insert into CAbmUserService values(217032707, 317032707, 1002, 20001230, 20391230);
            insert into CAbmUserService values(217032707, 317032707, 1003, 20001230, 20391230);
            delete from CAbmMonitorPlan where acct_id=217032707;
            insert into CAbmMonitorPlan values(217032707, 317032707, 20, 0, 1, 20021122, 20331122);
            exit''')
        str=str+"prepare data to abmmdb\n"
        if abmproc.returncode != 0:
            str=str+abmerr
        else:
            str=str+self.grep_mdb_str(abmout)  
        userproc=Popen(["mdb_client", self.ip,self.userport], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (userout, usererr) = userproc.communicate('''delete from CUser where m_llServId=317032707;
            insert into CUser values( 217032707, '991234217032707', '10168217032707', 317032707, 117032707, 5333932, 0, 0, 23, 0, 0, 1, 0, 2, 0, 0, '20170305090510', '20170108100807', '20170305090510', '20190316163001', 0, '20170305090510', 6);
            delete from CUserMsc where m_llServId=317032707;
            insert into CUserMsc values( 317032707, 317032707272238, 0, 102, 60002121, 1001, 20170108100807, 20170108100807, 20190316163001);
            delete from CUserProdSts where m_llServId=317032707;
            insert into CUserProdSts values( 317032707272238, 317032707, 50006, 1, 20170305090510, 20190316163001, 1002, 60002121);
            delete from CUserPay where m_llServId=317032707;
            insert into CUserPay values( 317032707, 217032707, 0, 999999999, 0, 1, 82000001, 1, 0, 0, 20170108100807, 20190316163001, 0, 0);
            delete from CUserCycle where m_llServId=317032707;
            insert into CUserCycle values( 317032707, 1, 20170305090510, 20190316163001, 1, 0, 0, 0);
            delete from CUserPlan where m_llServId=317032707;
            insert into CUserPlan values( 317032707, 1001, 23, 20170305090510, 20190316163001);            exit
            exit''')
        str=str+"prepare data to usermdb\n"
        if userproc.returncode != 0:
            str=str+usererr
        else:
            str=str+self.grep_mdb_str(userout) 
            
        rasproc=Popen(["mdb_client", self.ip,self.rasport], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (rasout, raserr) = rasproc.communicate('''delete from CRASBill where acct_id=217032707;
            insert into CRASBill values( 217032707, 317032707, 5006, 20170401, 20170501, 20170401, 20170501, 6, 0);
            delete from CRASBillDetail where bill_id=5006;
            insert into CRASBillDetail values( 5006, 505071, 30000, 0, 26000, 0, 0, 0, 0, 0);
            delete from CRASRentLog where acct_id=217032707;
            insert into CRASRentLog values( 317032707, 217032707, 60002121, 317032707272238, 5006, 60002121, 0, 2823, 0, 0, 0, 0, 20170108100807, 20190316163001);
            exit''')
        str=str+"prepare data to rasmdb\n"
        if rasproc.returncode != 0:
            str=str+raserr
        else:
            str=str+self.grep_mdb_str(rasout)     
            
        #修改日志级别
        logproc=Popen(["abm_mdb_param", "-i","/result/config/abm/abm_mdb_param.cfg"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (logout, logerr) = logproc.communicate('''2\nMonitorDebugFlag\n1\n3''')
        str=str+"prepare log level abmmdb\n"
        if logproc.returncode != 0:
            str=str+logerr
        else:
            str=str+self.grep_mdb_str(logout)     
            
        #修改账期
        monthproc=Popen(["ras_mdb_param", "-i","/result/config/aps50_ct/ras_mdb_param.cfg"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (monthout, montherr) = monthproc.communicate('''2\nBillDate1\n20170405\n2\nMonthCycle\n201704\n3''')
        str=str+"prepare log level abmmdb\n"
        if monthproc.returncode != 0:
            str=str+montherr
        else:
            str=str+self.grep_mdb_str(monthout)                                    
        return str 
    def select_table(self,port,table,cond,for_insert=False): 
        str=''
        userproc=Popen(["mdb_client", self.ip,port], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        cmd='select * from '+table+' '+cond+';\nexit\n';
        print cmd
        (userout, usererr) = userproc.communicate(cmd)
        str=str+"----------"+self.ip+":"+port+"--------select * from "+table+" "+cond+ "--------\n"
        if userproc.returncode != 0:
            str=str+usererr
        else:
            if for_insert:
                str=str+self.awk_v_str(self.grep_v_str(self.grep_str(self.grep_mdb_str(userout),','),'_oid'),',','insert into '+table+'  values(',[self.oidindex],');')
            else:   
                str=str+self.grep_mdb_str(userout) 
        return str 
    def select_ras_serv(self,port,serv_id,for_insert=False):
        str=''     
        rasout=self.select_table(port,'CRASBill','where serv_id=%s'%serv_id,for_insert) 
        str=str+rasout
        strtmp=self.awk_str(self.grep_v_str(self.grep_str(self.grep_mdb_str(rasout),','),'_oid'),',',[self.billidindex])
        patternlist=re.compile(r'\n')
        listtmp=patternlist.split(strtmp)
        for bill_id_tmp in listtmp:
                if bill_id_tmp:
                    str=str+self.select_table(port,'CRASBillDetail','where bill_id=%s'%bill_id_tmp,for_insert) 
        str=str+self.select_table(port,'CRASRentLog','where serv_id=%s'%serv_id,for_insert) 

        return str
        
    def select_abm_acct(self,port,acct_id,for_insert=False):   
        str=''     
        str=str+self.select_table(port,'CAbmUserService','where acct_id=%s'%acct_id,for_insert) 
        str=str+self.select_table(port,'CAbmMonitorQueue','where acct_id=%s'%acct_id,for_insert) 
        str=str+self.select_table(port,'CAbmZWMonitorQueue','where acct_id=%s'%acct_id,for_insert)
        str=str+self.select_table(port,'CAbmAlarmTrack','where acct_id=%s'%acct_id,for_insert) 
        str=str+self.select_table(port,'CAbmMonitorStatus','where acct_id=%s'%acct_id,for_insert) 
        str=str+self.select_table(port,'CAbmAcctLimit','where acct_id=%s'%acct_id,for_insert) 
        str=str+self.select_table(port,'CAbmMonitorPlan','where acct_id=%s'%acct_id,for_insert) 
        str=str+self.select_table(port,'CAbmCredit','where acct_id=%s'%acct_id,for_insert) 
        str=str+self.select_table(port,'CAbmBook','where acct_id=%s'%acct_id,for_insert) 
        str=str+self.select_table(port,'CAbmAlarm','where acct_id=%s'%acct_id,for_insert) 
        #str=str+self.select_table(port,'CAbmMdbParam','',for_insert) 
        return str
    def select_usermdb_serv(self,port,serv_id,for_insert=False):   
        str=''
        #str=str+self.select_table(port,'CUisPara','',for_insert)
        #str=str+self.select_table(port,'CServPara','',for_insert)
        str=str+self.select_table(port,'CUser','where m_llServId=%s'%serv_id,for_insert)
        str=str+self.select_table(port,'CUserMsc','where m_llServId=%s'%serv_id,for_insert)
        str=str+self.select_table(port,'CUserProdSts','where m_llServId=%s'%serv_id,for_insert)
        #str=str+self.select_table(port,'CPromPara','where m_llServId=%s'%serv_id,for_insert)
        str=str+self.select_table(port,'CUserPay','where m_llServId=%s'%serv_id,for_insert)
        str=str+self.select_table(port,'CUserCycle','where m_llServId=%s'%serv_id,for_insert)
        str=str+self.select_table(port,'CUserProm','where m_llServId=%s'%serv_id,for_insert)
        str=str+self.select_table(port,'CUserPlan','where m_llServId=%s'%serv_id,for_insert)
        return str
    def select_mdbdata(self,datas):
        serv_id=0;
        acct_id=0;
        for_insert=False
        if  self.re_get_param(datas,'serv_id'):           
            serv_id=self.re_get_param(datas,'serv_id')
        if  self.re_get_param(datas,'acct_id'):           
            acct_id=self.re_get_param(datas,'acct_id')
        if self.re_is_have(datas, 'for_insert'):
            for_insert=True           
        str=''
        #查询user_mdb中的数据
        print "begin to query user_mdb"
        if serv_id>0:
            str=str+self.select_usermdb_serv(self.userport,serv_id,for_insert) 
        elif acct_id>0:
            userout=self.select_table(self.userport,'CUser','where m_llAcctId=%s'%acct_id)
            strtmp=self.awk_str(self.grep_v_str(self.grep_str(self.grep_mdb_str(userout),','),'_oid'),',',[self.servidindex])
            patternlist=re.compile(r'\n')
            listtmp=patternlist.split(strtmp)
            for serv_id_tmp in listtmp:
                if serv_id_tmp:
                    str=str+self.select_usermdb_serv(self.userport,serv_id_tmp,for_insert) 
        #查询abm_mdb中数据
        print "begin to query abm_mdb"
        if acct_id>0:
            str=str+self.select_abm_acct(self.abmport,acct_id,for_insert) 
        elif serv_id>0:
            abmout=self.select_table(self.abmport,'CAbmUserService','where serv_id=%s'%serv_id)
            strtmp=self.awk_str(self.grep_v_str(self.grep_str(self.grep_mdb_str(abmout),','),'_oid'),',',[self.acctidindex])
            patternlist=re.compile(r'\n')
            listtmp=patternlist.split(strtmp)
            for acct_id_tmp in listtmp:
                if acct_id_tmp:
                    str=str+self.select_abm_acct(self.abmport,acct_id_tmp,for_insert)             
        #查询ras_mdb中数据
        print "begin to query ras_mdb"
        if serv_id>0:
            str=str+self.select_ras_serv(self.rasport,serv_id) 
        elif acct_id>0:
            userout=self.select_table(self.userport,'CUser','where m_llAcctId=%s'%acct_id)
            strtmp=self.awk_str(self.grep_v_str(self.grep_str(self.grep_mdb_str(userout),','),'_oid'),',',[self.servidindex])
            patternlist=re.compile(r'\n')
            listtmp=patternlist.split(strtmp)
            for serv_id_tmp in listtmp:
                if serv_id_tmp:
                    str=str+self.select_ras_serv(self.rasport,serv_id_tmp,for_insert)              
            
        print str               
        return str          
    def deal_mdb_data(self,path,datas):
        print path;
        print datas;
        pattern=re.compile(r'qr/=([\w]+)')
        list=pattern.findall(datas)
        print list
        switch={
                'set_env':self.set_env,
                'insert_CAbmMonitorQueue':self.insert_CAbmMonitorQueue,
                'select_mdbdata':self.select_mdbdata, 
                'prepare_mdbdata':self.prepare_mdbdata              
                }
        str='';
        for deal_data in list:
            print "start %s begin"%deal_data
            out=switch[deal_data](datas)
            str=str+self.transfer_br(out)
            print "start %s end"%deal_data
        html_from=""
        buf = self.return_page%("deal_mdb_data ",str,path,html_from) 
        return buf   
        
    