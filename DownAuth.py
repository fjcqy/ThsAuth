#!/usr/bin/env python
# -*- coding: cp936 -*-

#日期：2016/12/10
#作者：chenquanying
#邮箱：371918080@qq.com
#作用：批量下载证书
#版本：1.2

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

#获取当前目录
def get_file():
    rootdir = os.getcwd()
    print '当前目录：\n' + rootdir

    #遍历所以文件，包括子目录
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            #只读取后缀为'.txt'的文件
            if os.path.splitext(filename)[1] == '.txt':
                print '\n读取文件：\n' + os.path.join(parent,filename) + '\n'
                read_file(parent,filename)

#读取文件
def read_file(parent,filename):
    dir_file = os.path.join(parent,filename)
    fobj = open(dir_file, 'r')
    allLines = fobj.readlines()     #读完所有行
    fobj.close()
    for eachLine in allLines:       #遍历整个文件
        #标准authcode示例：M11-v4qp-jP+w-PLc8-b3oA-lXZE
        #判断每行第4、第9个字符是否为'-'，否则不是合法authcode
        if eachLine[3:4] == '-' and eachLine[8:9] == '-':
            #产品证书
            authcode = eachLine[0:28]   #取前28个字符
            print authcode
            down_file(parent,authcode)
        else:
            continue

#下载证书
def down_file(parent,authcode):

    #对authcode进行url编码处理
    authcode = code2url(authcode)
    #print 'authcode处理后：' + authcode

    search_url='http://services.myhexin.com/produser/querycert?authcode=' + authcode + '&Create=%B2%E9%D1%AF'
    print '查询地址：\n' + search_url

    #打开查询页面
    try:
        webpage = urlopen(search_url)
        webpage.close()
    except:
        print '错误：查询地址打开失败。\n'
    
    #模拟人操作，延时0.5秒
    time.sleep(0.5)

    download_url='http://services.myhexin.com/produser/downloadcert?libver=20030506&authcode=' + authcode + '&Submit=%CF%C2%D4%D8%D6%A4%CA%E9'
    print '下载地址：\n' + download_url

    download_file=authcode[0:3] + '.dat'
    print '文件名：' + download_file + '\n'

    #下载证书文件
    times = 1
    while times <=3:
        try:
            urlretrieve(download_url, os.path.join(parent,download_file))
            confirm(parent,download_file)
            #如果下载成功并验证通过，才会break
            break
        except:
            print '%s%d%s' % ('错误：下载超时，次数：', times, '\n')
            if times == 3:
                global errorfile
                errorfile += os.path.join(parent,download_file) + ' 下载失败！' + '\n'
            times += 1

def confirm(parent,download_file):
    #对下载的证书文件进行判断
    fobj = open(os.path.join(parent,download_file), 'r')
    firstline = fobj.readline()
    #下载的证书前8个字符一定是'PRODCERT'
    if firstline[0:8] != 'PRODCERT':
        global errorfile
        errorfile += os.path.join(parent,download_file) + '验证不通过！' + '\n'
    fobj.close()

#对authcode进行url编码处理
def code2url(authcode):
    #将'+'替换成'%2B'
    authcode = authcode.replace('+','%2B')
    return authcode

print '''
请按下面要求，否则无法自动下载证书：
1、将需要下载的产品证书保存在*.txt文本中，名字随意
2、*.txt中每个产品证书一行，需保证产品证书在每行开头
3、每台要下载证书的服务器保存一个*.txt文件
4、每个*.txt保存在一个文件夹，否则会发生覆盖
5、下载的证书会根据证书自动命名，并和*.txt保存在同一个目录下
6、请避免在网络极度不好时使用本脚本，以免下载失败
7、其他请参考压缩包格式
'''
if raw_input('按y继续，其他任意键退出：') == 'y':
    get_file()
    print '下列产品证书下载失败，请手动下载：\n' + errorfile
    if errorfile == '':
        print '全部下载成功\n'
    else:
        print '1、请确认"验证不通过"的证书是否是已注销等原因。\n2、网络不好、服务器未响应都会造成下载失败。\n3、否则，请将错误的产品证书提交给QQ：371918080，以便排查错误。\n'
    raw_input('按任意键继续。。。')
