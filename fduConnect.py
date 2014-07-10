#!/usr/bin/python
#encoding:utf-8

import re

from bs4 import BeautifulSoup

from web import Web

class FduConnect:
    def __init__(self, username, password):
        self.__login(username, password)

        self.__exerLogined = False

    def __del__(self):
        self.__logout()

    def __login(self, username, password):
        loginUrl = 'https://uis1.fudan.edu.cn/amserver/UI/Login'
        data = {"IDToken0" : "", "IDToken1" : username, "IDToken2" : password, \
            "IDButton" : "Submit", "goto" : "", "encoded" : "false", \
            "inputCode" : "", "gx_charset" : "UTF-8"}
        self.__connect = Web(loginUrl, data)

    def __logout(self):
        logoutUrl = 'http://www.portal.fudan.edu.cn/main/logout.do'
        self.__connect.logout(logoutUrl)

    def __loginExercise(self):
        url = 'http://www.fdty.fudan.edu.cn/sportscore/'
        content = self.__connect.open(url)
        if content == None:
            return

        soup = BeautifulSoup(content)
        result = soup.find('input', id = '__VIEWSTATE')
        viewstate = result['value']
        result = soup.find('input', id = '__EVENTVALIDATION')
        eventvalidation = result['value']

        url = 'http://www.fdty.fudan.edu.cn/sportscore/default.aspx'
        data = {"__EVENTTARGET" : "", "__EVENTARGUMENT" : "", "__LASTFOCUS" : "", \
            "__VIEWSTATE" : viewstate, "__EVENTVALIDATION" : eventvalidation, \
            "dlljs" : "st", "Button1" : ""}
        self.__connect.open(url, data)

    def getExercise(self):
        if (self.__exerLogined == False):
            self.__loginExercise()
            self.__exerLogined = True

        url = 'http://www.fdty.fudan.edu.cn/sportScore/stScore.aspx'
        content = self.__connect.open(url)
        if content == None:
            return []

        soup = BeautifulSoup(content)
        result = soup.find('span', id = 'lblmsg')

        pattern = re.compile(u'>.{,10}</td>')
        resList = pattern.findall(unicode(result))
        ans = []
        for i in xrange(0, len(resList) - 1, 2):
            key = resList[i]
            value = resList[i + 1]
            ans.append((key[1 : len(key) - 5], value[1 : len(value) - 5]))

        return ans

    def getGPA(self):
        url = 'http://www.urp.fudan.edu.cn:78/epstar/app/fudan/ScoreManger/ScoreViewer/Student/Course.jsp'
        content = self.__connect.open(url)
        if content == None:
            return []

        soup = BeautifulSoup(content)
        result = soup.find('tr', id = 'tr_0')

        ans = []
        while result != None:
            course = []
            row = result.contents
            for i in xrange(1, len(row), 2):
                course.append(row[i].string.replace('\t', '').replace('\r', '').replace('\n', ''))
            ans.append(tuple(course))
            result = result.nextSibling.nextSibling

        return ans
