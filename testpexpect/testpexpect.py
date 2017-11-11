#coding=UTF-8

import pexpect

PROMPT = ['#','>>>','>','\$']

def send_command(child,cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print child.before,child.buffer

def connect(user,host,password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = 'ssh '+user+'@'+host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT,ssh_newkey,'[p|P]assword:'])
    if ret == 0:
        print('[-] Error Connecting')
        return
    if ret == 1:
        child.sendline('yes')
        ret =child.expect([pexpect.TIMEOUT,'[p|P]assword:'])
    if ret == 0:
        print('[-] Error Connecting')
        return
    child.sendline(password)
    child.expect(PROMPT)
    return child

def main():
    host = '192.168.191.5'
    user='root'
    password='toor'
    child=connect(user,host,password)
    send_command(child,'cat /etc/shadow | grep root')

if __name__ == '__main__':
    main()
