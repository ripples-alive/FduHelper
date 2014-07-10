#!/usr/bin/python
#encoding:utf-8

import time
import getpass

from fduConnect import FduConnect
from fetion import Fetion
from log import writeLog

def getDiffExer(newExer, oldExer):
    isFirst = True
    s = ''
    for i in xrange(len(newExer)):
        if newExer[i] != oldExer[i]:
            if isFirst:
                isFirst = False
            else:
                s += '；'
            s += newExer[i][0] + newExer[i][1]
    return s

def getDiffGPA(newGPA, oldGPA):
    diff = set(newGPA) - set(oldGPA)
    isFirst = True
    s = ''
    for row in diff:
        if isFirst:
            isFirst = False
        else:
            s += '；'
        s += row[4] + '：' + row[6]
    return s

username = '12307130267'
password = getpass.getpass('请输入URP密码：')

connect = FduConnect(username, password)

exer = connect.getExercise()
for x in exer:
    print x[0] + x[1]
writeLog(exer)
exer[0] = exer[1] = (1, 2)

gpa = connect.getGPA()
for x in gpa:
    s = ''
    for y in x:
        s += y + '\t'
    print s
writeLog(gpa)
gpa = []

del(connect)

fetionUser = '18321985560'
fetionPwd = getpass.getpass('请输入飞信密码：')

fet = Fetion(fetionUser, fetionPwd)
fet.sendMsg('此短信仅为验证飞信密码、功能是否正常！')
del(fet)

while True:
    time.sleep(60)

    connect = FduConnect(username, password)

    result = connect.getExercise()
    if len(result) == len(exer) and set(result) != set(exer):
        print 'New exercise!'
        fet = Fetion(fetionUser, fetionPwd)
        # print '您的体锻有更新！' + getDiffExer(result, exer)
        fet.sendMsg('您的体锻有更新！' + getDiffExer(result, exer))
        del(fet)

        exer = result
        writeLog(exer)
    elif len(result) < len(exer):
        writeLog('There is something wrong with exercise.')
        writeLog(result)

    result = connect.getGPA()
    if len(result) > len(gpa):
        print 'New score!'
        fet = Fetion(fetionUser, fetionPwd)
        # print '您有新的科目出分了！' + getDiffGPA(result, gpa)
        fet.sendMsg('您有新的科目出分了！' + getDiffGPA(result, gpa))
        del(fet)

        gpa = result
        writeLog(gpa)
    elif len(result) < len(gpa):
        writeLog('There is something wrong with the scores.')
        writeLog(result)

    del(connect)
