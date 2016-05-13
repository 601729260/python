import dns.resolver
import datetime
import os
import pymongo
import threading

global THREADNUM
global querynum
global mutex


def timeinterval(funcname,func,param):
    begintime=datetime.datetime.now()
    answer=func(param)
    endtime=datetime.datetime.now()
    filename=os.getcwd()+'/'+'testdns.log'
    f=open(filename,'a')
    f.write(str(datetime.datetime.now())+' '+str(threading.currentThread().getName())+' '+funcname+'('+str(param)+') '+str(endtime-begintime)+'\n')

    return answer


def get_dnsip(urlname,list,my_resolver,querylayer):
    global THREADNUM
    for letter in list:
        url="www."+urlname+letter+".com"
        
        try:
            answer = timeinterval('dns.resolver.Resolver.query',my_resolver.query,url)
            client = pymongo.MongoClient("localhost", 27017)
            db = client.dns
            content={"name": url,"ip":str(answer[0])}
            timeinterval('db.ip.insert_one',db.ip.insert_one,content)
            mutex.acquire()
            global querynum
            querynum=querynum+1  
            print str(threading.currentThread().getName())+":"+url+":"+str(querylayer)+":"+str(querynum)+":"+str(THREADNUM)
            mutex.release()          
        except:
            if querynum==300:
                os._exit(0) 
            continue
        if querynum==300:
            os._exit(0)
            
        
    for letter in list:
        querylaye2=querylayer+1
        if THREADNUM<10:
            mutex.acquire()
            THREADNUM=THREADNUM+1
            mutex.release()
            threading.Thread(target=get_dnsip,args=(urlname+letter,list,my_resolver,querylaye2)).start()
    
    if threading.currentThread().getName()!="MainThread":
        mutex.acquire()
        THREADNUM=THREADNUM-1
        mutex.release()
if __name__ == '__main__':
    pass
    my_resolver = dns.resolver.Resolver()
    querylayer=0
    THREADNUM=0
    querynum=0
    list=[]
    for i in range(65,91):
        list+=chr(i)
    for i in range(0,10):
        list+=str(i)
    mutex = threading.Lock()   
    get_dnsip("",list,my_resolver,querylayer) 
