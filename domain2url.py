#!/usr/bin/python3
# coding: utf-8
# Author: EMo
import http.client,sys
import threading
import threadpool
from functools import wraps
import datetime

datas = list()

def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        print(func.__name__, end-start)
        return result
    return wrapper

def get_url(host):
    """ 将域名转换为URL（是否协议与WWW判断） """
    global datas
    conn = http.client.HTTPConnection(host,timeout=3)
    try:
        conn.request("HEAD",'')
    except Exception as TE:
        print(("1",host,TE))
        host = "www."+host
        conn = http.client.HTTPConnection(host,timeout=3)
        try:
            conn.request("HEAD",'')
        except Exception as TE:
            print(("2",host,TE))
    try:
        conn.getresponse()
        ret = "http://"+host
    except Exception as TE:
        print(("3",host,TE))
        ret = "https://"+host
    datas.append(ret)
    print(ret)

@timethis
def main():
    thdpol = threadpool.ThreadPool(10)
    if not (sys.argv[1][-4:] == "list" or sys.argv[1][-3:] == "txt"):
        get_url(sys.argv[1])
    else:
        try:
            with open(sys.argv[1],"r") as f:
                argslist = f.read().splitlines()
                """ 此处多线程操作 """
                threadRequests = threadpool.makeRequests(get_url,argslist)
                for request in threadRequests:
                    thdpol.putRequest(request)
                thdpol.wait()
        finally:
            print(datas,len(datas))

if __name__ == '__main__':
    main()
# >>> response = requests.get('http://quora.com', stream=True)
# >>> response.raw._connection.sock.getpeername()