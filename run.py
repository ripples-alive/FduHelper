#!/usr/bin/python
#encoding:utf-8

import time
import getpass

from fduConnect import FduConnect
from fetion import Fetion

connect = FduConnect()
connect.login('12307130267', getpass.getpass('请输入URP密码：'))

exer = connect.getExercise()
for x in exer:
    print x[0] + x[1]

gpa = connect.getGPA()
for x in gpa:
    s = ''
    for y in x:
        s += y + '\t'
    print s

fet = Fetion('18321985560', getpass.getpass('请输入飞信密码：'))

while True:
    time.sleep(60)

    result = connect.getExercise()
    if result != exer:
        print 'New exercise!'
        fet.sendMsg('您的体锻有更新！')

        exer = result

    result = connect.getGPA()
    if result != gpa:
        print 'New score!'
        fet.sendMsg('您有新的科目出分了！')

        gpa = result
