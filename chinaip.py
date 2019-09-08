#!/usr/bin/env python
#fileencoding: utf-8
#Author: Liu DongMiao <liudongmiao@gmail.com>
#Created  : TIMESTAMP
#Modified : TIMESTAMP
import sys
import socket
import struct
import urllib
MAXBITS = 12
getip = lambda x: socket.inet_ntoa(struct.pack('!I', x))
getint = lambda x: struct.unpack('!I', socket.inet_aton(x))[0]
def exchange_maskint(mask_int):
    bin_arr = ['0' for i in range(32)]
    for i in range(mask_int):
        bin_arr[i] = '1'
    tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
    return '.'.join(tmpmask)
def chinaip(start,end):
    base = start
    while base <= end:
        step = 0
        while (base | (1 << step)) != base:
            if (base | (0xffffffff >> (31 - step))) > end:
                break
            step += 1
        if step >= (32 - MAXBITS):
            chinaips.append(('%s %s') % (getip(base), exchange_maskint(32 - step)))
        base += (1 << step)
def check_range(start, end):
    count = 0
    base = start
    while base <= end:
        step = 0
        while (base | (1 << step)) != base:
            if (base | (0xffffffff >> (31 - step))) > end:
                break
            step += 1
        if step >= (32 - MAXBITS):
            count += (1 << step)
            # print ('%s/%s') % (getip(base), (32 - step))
        base += (1 << step)
    return count
def parse_record(name):
    routed = 0
    amount = 0
    start = end = 0
    for x in open(name):
        # apnic|CN|ipv4|1.0.1.0|256|20110414|allocated
        if 'CN|ipv4' not in x:
            continue
        lists = x.split('|')
        ip = lists[3]
        count = int(lists[4])
        newstart = getint(ip)
        newend = newstart + count
        if end == newstart:
            end = newend
        else:
            if end - start + 1 >= (1 << (32 - MAXBITS)):
                chinaip(start,end-1)
                routed += check_range(start, end - 1)
            amount += end - start
            start = newstart
            end = newend
    # print(chinaips)
    with open ('chinaip_openvpn_server.txt','w') as f:
        result=''
        for ip in chinaips:
            result+=("push \"route %s net_gateway\"\n"%ip)
        # print(result)
        f.write(result)
    with open ('chinaip_openvpn_client.txt','w') as f:
        result=''
        for ip in chinaips:
            result+=("route %s net_gateway\n"%ip)
        # print(result)
        f.write(result)
    print >> sys.stderr, 'size:%d %d%%' % (len(chinaips),100 * routed / amount)
    # print >> sys.stderr, 'routed=%d, amount=%d' % (routed, amount)
DELEGATED_APNIC = 'http://ftp.apnic.net/stats/apnic/delegated-apnic-latest'
if __name__ == '__main__':
    chinaips=['10.0.0.0 255.255.0.0','172.16.0.0 255.240.0.0','192.168.0.0 255.255.0.0']
    if len(sys.argv) == 1:
        # with urllib.urlopen(DELEGATED_APNIC) as uo:
        #     print(uo.read())
        urllib.urlretrieve(DELEGATED_APNIC,'delegated-apnic-latest')
        parse_record('delegated-apnic-latest')
        # print >> sys.stderr, 'please download %s' % DELEGATED_APNIC
    else:
        if len(sys.argv) > 2:
            MAXBITS = int(sys.argv[2])
        parse_record(sys.argv[1])
# vim: set sta sw=4 et:
