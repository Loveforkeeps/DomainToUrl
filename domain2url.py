#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Erdog

import http.client, sys
import threadpool
import datetime
from socket import timeout as TIMEOUT_ERRO
from socket import gaierror as GETADDRINFO_ERRO
import argparse


# 时间装饰器
def functime(func):
    def wap(*args, **kw):
        local_time = datetime.datetime.now()
        func(*args, **kw)
        times = (datetime.datetime.now() - local_time).seconds
        print('Run time is {} minutes {} seconds'.format(
            times // 60, times % 60))

    return wap


class GetUrl():
    """ 将域名转换为Url:是否加密协议与WWW判断
    args:
        domain, 域名
        byproxy, 是否使用代理
    """
    # 请求头
    Headers = {
        "Upgrade-Insecure-Requests": '1',
        "User-Agent":
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Connection": "close"
    }

    # 代理设置
    proxyip = None
    proxyport = None
    byproxy = False

    # 请求设置
    timeout = 15

    def __init__(self, domain):
        self.domain = domain
        self.url = self.resquest(domain)

    @classmethod
    def setProxy(GetUrl, proxyip=None, proxyport=None):
        """ 设置代理 """
        if proxyip == None:
            proxyip = GetUrl.proxyip
        if proxyport == None:
            proxyport = GetUrl.proxyport
        GetUrl.byproxy = True
        GetUrl.proxyip = proxyip
        GetUrl.proxyport = proxyport

    def resquest(self, host):
        """ 获取Url """
        # 发起请求
        conn = self.get_conn()
        ret = "http://" + host
        try:
            conn.request('HEAD', '', headers=self.Headers)
        except GETADDRINFO_ERRO:
            print(host + ' DNS查询异样,无法解析域名')
            return ret
        except TIMEOUT_ERRO:
            print(host + ' 请求超时')
            return ret
        except Exception as TE:
            print("1", host, TE)
            host = "www." + host
            conn = self.get_conn()
            try:
                conn.request("HEAD", '', headers=self.Headers)
            except Exception as TE:
                print("2", host, TE)
        # 处理请求返回
        try:
            _hr = conn.getresponse()
            if _hr.status in [301, 302, 307, 308]:
                location = _hr.getheader('Location')
                print(host, _hr.status, _hr.reason)
            else:
                if _hr.status >= 400 or _hr.status >= 500:
                    print(host, _hr.status, _hr.reason)
                    try:
                        conn = self.get_conn()
                        conn.request('GET', '', headers=self.Headers)
                        _hr = conn.getresponse()
                        if _hr.status in [301, 302, 307, 308]:
                            location = _hr.getheader('Location')
                    except Exception as e:
                        print(host, e)
            if 'location' in locals():
                if location.startswith("/"):
                    ret = ret + location
                else:
                    if location.startswith("http://") or location.startswith("https://"):
                        ret = location
                    else:
                        ret = ret + '/' + location
        finally:
            return ret
    
    

    def get_conn(self, host=None):
        """ 获取配置好的HTTPConnection """
        if not host:
            host = self.domain
        if self.byproxy:
            conn = http.client.HTTPConnection(self.proxyip,
                                              self.proxyport,
                                              timeout=self.timeout)
            conn.set_tunnel(host)
        else:
            conn = http.client.HTTPConnection(host, timeout=self.timeout)
        return conn


def worker(domain):
    a = GetUrl(domain)
    # print(a.url)
    global urllist
    urllist.append(a.domain + ' : ' + a.url)
    return a.url


@functime
def main():
    thdpol = threadpool.ThreadPool(args.tn)
    if args.debug == 'proxy':
        GetUrl.proxyip = args.host
        GetUrl.proxyport = args.port
        GetUrl.setProxy()
    GetUrl.timeout = 15

    if args.domain:
        domain = args.domain
        print(GetUrl(domain).url)
        # worker(domain)
    if args.file:
        try:
            argslist = args.file.read().splitlines()
            threadRequests = threadpool.makeRequests(worker, argslist)
            for request in threadRequests:
                thdpol.putRequest(request)
            thdpol.wait()
        except KeyboardInterrupt:
            sys.exit(127)
        finally:
            print(urllist, len(urllist))
            with open(args.file.name + '.url.txt', 'w') as f:
                f.writelines('\n'.join(urllist))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=u'将Domain动态转化为Url',
                                     add_help=False)
    parser.add_argument('-h', '--help', action='help', help=u'显示帮助信息')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f',
                       '--file',
                       type=argparse.FileType('r'),
                       help=u'选定要转换的域名文件(按行分割)')
    group.add_argument('-d', dest='domain', type=str, help=u'直接指定域名进行转换')

    parser.add_argument('-tn', type=int, default=50, help=u'指定线程数,默认50')

    sub = parser.add_subparsers(title=u'debug arguments', dest='debug')
    proxy = sub.add_parser('proxy', help=u'Proxy IP Port')
    proxy.add_argument('host', help=u'Proxy IP')
    proxy.add_argument('port', help=u'Proxy Port')

    args = parser.parse_args()

    # print(args)
    # Url结果存放
    urllist = list()
    main()