#!/usr/bin/python
#encoding:utf-8

import time
import getpass

from fduConnect import FduConnect
from fetion import Fetion
from log import write_log


def get_diff_exercise(new_exercise, old_exercise):
    """Get the difference between the new and old information if exercise."""
    is_first = True
    s = ''
    for i in xrange(len(new_exercise)):
        if new_exercise[i] != old_exercise[i]:
            if is_first:
                is_first = False
            else:
                s += '；'
            s += new_exercise[i][0] + new_exercise[i][1]
    return s


def get_diff_gpa(new_gpa, old_gpa):
    """Get the scores appeared newly."""
    diff = set(new_gpa) - set(old_gpa)
    is_first = True
    s = ''
    for row in diff:
        if is_first:
            is_first = False
        else:
            s += '；'
        s += row[4] + '：' + row[6]
    return s


# Get URP password and connect to the URP.
username = '12307130267'
password = getpass.getpass('请输入URP密码：')
connect = FduConnect(username, password)

exercise = connect.get_exercise()
for x in exercise:
    print x[0] + x[1]
write_log(exercise)
# exercise[0] = exercise[1] = (1, 2)

gpa = connect.get_gpa()
for x in gpa:
    s = ''
    for y in x:
        s += y + '\t'
    print s
write_log(gpa)
# gpa = []

del connect

# Get the fetion password and try to send a message.
fet_user = '18321985560'
fet_pwd = getpass.getpass('请输入飞信密码：')
fet = Fetion(fet_user, fet_pwd)
fet.send_msg('此短信仅为验证飞信密码、功能是否正常！')
# Delete to logout. Avoid affecting the normal use of fetion.
del fet

while True:
    time.sleep(60)

    connect = FduConnect(username, password)

    result = connect.get_exercise()
    if len(result) == len(exercise) and set(result) != set(exercise):
        # The information of exercise has changed. Notify the user.
        print 'New exercise!'
        fet = Fetion(fet_user, fet_pwd)
        # print '您的体锻有更新！' + get_diff_exercise(result, exercise)
        fet.send_msg('您的体锻有更新！' + get_diff_exercise(result, exercise))
        del fet

        exercise = result
        write_log(exercise)
    elif len(result) < len(exercise):
        # There is something wrong with the new enquiry.
        write_log('There is something wrong with exercise.')
        write_log(result)

    result = connect.get_gpa()
    if len(result) > len(gpa):
        # The information of scores has changed. Notify the user.
        print 'New score!'
        fet = Fetion(fet_user, fet_pwd)
        # print '您有新的科目出分了！' + get_diff_gpa(result, gpa)
        fet.send_msg('您有新的科目出分了！' + get_diff_gpa(result, gpa))
        del fet

        gpa = result
        write_log(gpa)
    elif len(result) < len(gpa):
        # There is something wrong with the new enquiry.
        write_log('There is something wrong with the scores.')
        write_log(result)

    del connect
