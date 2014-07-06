#!/usr/bin/python
#encoding:utf-8

import time
import getpass

from fduConnect import FduConnect
from fetion import Fetion
from log import writeLog

connect = FduConnect()
connect.login('12307130267', getpass.getpass('请输入URP密码：'))

exer = connect.getExercise()
for x in exer:
    print x[0] + x[1]
writeLog(exer)

gpa = connect.getGPA()
for x in gpa:
    s = ''
    for y in x:
        s += y + '\t'
    print s
writeLog(gpa)

fet = Fetion('18321985560', getpass.getpass('请输入飞信密码：'))
fet.sendMsg('此短信仅为验证飞信密码、功能是否正常！')

while True:
    time.sleep(60)

    result = connect.getExercise()
    if len(result) == len(exer) and result != exer:
        print 'New exercise!'
        fet.sendMsg('您的体锻有更新！')

        exer = result
        writeLog(exer)
    elif len(result) < len(exer):
        writeLog('There is something wrong with exercise.')
        writeLog(result)

    result = connect.getGPA()
    if len(result) > len(gpa):
        print 'New score!'
        fet.sendMsg('您有新的科目出分了！')

        gpa = result
        writeLog(gpa)
    elif len(result) < len(gpa):
        writeLog('There is something wrong with the scores.')
        writeLog(result)
