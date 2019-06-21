# DomainToUrl
将域名转换为URL（HTTPS/HTTP,WWW）

## Using:

```
usage: domain2url.py [-h] [-f FILE | -d DOMAIN] [-tn TN] {proxy} ...

将Domain动态转化为Url

optional arguments:
  -h, --help            显示帮助信息
  -f FILE, --file FILE  选定要转换的域名文件(按行分割)
  -d DOMAIN             直接指定域名进行转换
  -tn TN                指定线程数,默认50

debug arguments:
  {proxy}
    proxy               Proxy IP Port
```

sample:

```
 python3 domain2urlClass.py -f 1000.txt -tn 100 proxy 127.0.0.1 8080 
```

