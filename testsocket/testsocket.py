# -*- coding: utf-8 -*- #

#服务器及端口扫描

#套接字模块提供了一个可以使 python 建立网络连接的库。
# 让我们快速的编写一个获 取提示信息的脚本，连接到特定 IP 地址和端口后，
# 我们的脚本将打印提示信息，之后， 我们使用 connect()函数连接到 IP 地址和端口。
# 一旦连接成功，就可以通过套接字进 行读写。这种 recv(1024)的方法将读取之后在套接字中 1024 字节的数据。
# 我们把这种方式的结果存到一个变量中，然后打印到服务器。
import socket

#内置的 sys 模块提供访问和维护 python 解释器的能力。
# 这包括了提示信息，版本， 整数的最大值，可用模块，路径钩子，标准错误，
# 标准输入输出的定位和解释器调用 的命令行参数。
import sys

#内置的 OS 模块提供了丰富的与 MAC,NT,Posix 等操作系统进行交互的能力。
# 这个模块允许程序独立的与操作系统环境。文件系统，用户数据库和权限进行交互。
# 思考一 下，比如，上一章中，用户把文件名作为命令行参数来传递。他可以验证文件是否存
# 在以及当前用户是否有权限都这个文件。如果失败，他将显示一条信息，来显示一个 适当的错误信息给用户。
import os

#读取有漏洞的服务信息
if len(sys.argv) == 2:
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print '[-] '+filename+'does not exist.'
        exit(0)
    print '[+] Reading Vulnerabilities From: ' + filename
else:
    filename = 'vuln_banners.txt'
    print  '[-] Reading Vulnerabilities From default file'

#返回连接信息
def retBanner(ip,port):
    socket.setdefaulttimeout(2)
    s=socket.socket()
    try:
        s.connect((ip,int(port)))
        banner = s.recv(1024)
        return banner
    except Exception,e:
        #python 语言提供的异常处理能力。我们使用 try/except 进行异常处理。
        # 当错误发生时，我们的异常处理捕获 错误并把错误信息打印到屏幕上。
        #print '[-] Error = '+str(e)
        return

#扫描可攻击服务端口
def checkVulnerables(banner):
    f=open(filename,'r')
    for line in f.readlines():
        #必须用方法.strip(‘\r’)去掉每行的回车符，如果发 现一对匹配了，我们打印出有漏洞的服务信息。
        if line.strip('\n') in banner:
            print '[+] Server is vulnerable: '+banner.strip('\n')

#循环扫描服务端口
def loopcheck(ip,portList):
    for x in range(1,255):
        for port in portList:
            print '[+] Checking '+ip\
            +str(x)+':'+str(port)
            banner=retBanner(ip+str(x),str(port))
            if banner:
                checkVulnerables(banner)

def main():

    loopcheck('172.18.72.',[21,22,80,110])

if __name__=='__main__':
    main()
