#!/usr/bin/env python
# -*- coding: cp936 -*-

#���ڣ�2016/12/10
#���ߣ�chenquanying
#���䣺371918080@qq.com
#���ã���������֤��
#�汾��1.2

from urllib import urlopen
from urllib import urlretrieve

import os
import os.path

from os.path import getsize

import time

import socket
socket.setdefaulttimeout(6)

global errorfile
errorfile = ''

#��ȡ��ǰĿ¼
def get_file():
    rootdir = os.getcwd()
    print '��ǰĿ¼��\n' + rootdir

    #���������ļ���������Ŀ¼
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            #ֻ��ȡ��׺Ϊ'.txt'���ļ�
            if os.path.splitext(filename)[1] == '.txt':
                print '\n��ȡ�ļ���\n' + os.path.join(parent,filename) + '\n'
                read_file(parent,filename)

#��ȡ�ļ�
def read_file(parent,filename):
    dir_file = os.path.join(parent,filename)
    fobj = open(dir_file, 'r')
    allLines = fobj.readlines()     #����������
    fobj.close()
    for eachLine in allLines:       #���������ļ�
        #��׼authcodeʾ����M11-v4qp-jP+w-PLc8-b3oA-lXZE
        #�ж�ÿ�е�4����9���ַ��Ƿ�Ϊ'-'�������ǺϷ�authcode
        if eachLine[3:4] == '-' and eachLine[8:9] == '-':
            #��Ʒ֤��
            authcode = eachLine[0:28]   #ȡǰ28���ַ�
            print authcode
            down_file(parent,authcode)
        else:
            continue

#����֤��
def down_file(parent,authcode):

    #��authcode����url���봦��
    authcode = code2url(authcode)
    #print 'authcode�����' + authcode

    search_url='http://services.myhexin.com/produser/querycert?authcode=' + authcode + '&Create=%B2%E9%D1%AF'
    print '��ѯ��ַ��\n' + search_url

    #�򿪲�ѯҳ��
    try:
        webpage = urlopen(search_url)
        webpage.close()
    except:
        print '���󣺲�ѯ��ַ��ʧ�ܡ�\n'
    
    #ģ���˲�������ʱ0.5��
    time.sleep(0.5)

    download_url='http://services.myhexin.com/produser/downloadcert?libver=20030506&authcode=' + authcode + '&Submit=%CF%C2%D4%D8%D6%A4%CA%E9'
    print '���ص�ַ��\n' + download_url

    download_file=authcode[0:3] + '.dat'
    print '�ļ�����' + download_file + '\n'

    #����֤���ļ�
    times = 1
    while times <=3:
        try:
            urlretrieve(download_url, os.path.join(parent,download_file))
            confirm(parent,download_file)
            #������سɹ�����֤ͨ�����Ż�break
            break
        except:
            print '%s%d%s' % ('�������س�ʱ��������', times, '\n')
            if times == 3:
                global errorfile
                errorfile += os.path.join(parent,download_file) + ' ����ʧ�ܣ�' + '\n'
            times += 1

def confirm(parent,download_file):
    #�����ص�֤���ļ������ж�
    fobj = open(os.path.join(parent,download_file), 'r')
    firstline = fobj.readline()
    #���ص�֤��ǰ8���ַ�һ����'PRODCERT'
    if firstline[0:8] != 'PRODCERT':
        global errorfile
        errorfile += os.path.join(parent,download_file) + '��֤��ͨ����' + '\n'
    fobj.close()

#��authcode����url���봦��
def code2url(authcode):
    #��'+'�滻��'%2B'
    authcode = authcode.replace('+','%2B')
    return authcode

print '''
�밴����Ҫ�󣬷����޷��Զ�����֤�飺
1������Ҫ���صĲ�Ʒ֤�鱣����*.txt�ı��У���������
2��*.txt��ÿ����Ʒ֤��һ�У��豣֤��Ʒ֤����ÿ�п�ͷ
3��ÿ̨Ҫ����֤��ķ���������һ��*.txt�ļ�
4��ÿ��*.txt������һ���ļ��У�����ᷢ������
5�����ص�֤������֤���Զ�����������*.txt������ͬһ��Ŀ¼��
6������������缫�Ȳ���ʱʹ�ñ��ű�����������ʧ��
7��������ο�ѹ������ʽ
'''
if raw_input('��y����������������˳���') == 'y':
    get_file()
    print '���в�Ʒ֤������ʧ�ܣ����ֶ����أ�\n' + errorfile
    if errorfile == '':
        print 'ȫ�����سɹ�\n'
    else:
        print '1����ȷ��"��֤��ͨ��"��֤���Ƿ�����ע����ԭ��\n2�����粻�á�������δ��Ӧ�����������ʧ�ܡ�\n3�������뽫����Ĳ�Ʒ֤���ύ��QQ��371918080���Ա��Ų����\n'
    raw_input('�����������������')
