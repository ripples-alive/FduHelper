#!/usr/bin/python
#encoding:utf-8

import re

from bs4 import BeautifulSoup

from web import Web


class FduConnect:
    """Class to connect to the website of Fudan University."""
    def __init__(self, username, password):
        """Init the specified username and password."""
        self.__login(username, password)

        self.__exercise_is_login = False

    def __del__(self):
        # Auto logout when destroy.
        self.__logout()

    def __login(self, username, password):
        # Login URP with specified username and password.
        login_url = 'https://uis1.fudan.edu.cn/amserver/UI/Login'
        data = {"IDToken0": "", "IDToken1": username, "IDToken2": password,
                "IDButton": "Submit", "goto": "", "encoded": "false",
                "inputCode": "", "gx_charset": "UTF-8"}
        self.__connect = Web(login_url, data)

    def __logout(self):
        logout_url = 'http://www.portal.fudan.edu.cn/main/logout.do'
        self.__connect.logout(logout_url)

    def __login_exercise(self):
        # Login to the exercise system.
        url = 'http://www.fdty.fudan.edu.cn/sportscore/'
        content = self.__connect.open(url)
        if content is None:
            return

        # Get the value of __VIEWSTATE and __EVENTVALIDATION for login.
        soup = BeautifulSoup(content)
        result = soup.find('input', id='__VIEWSTATE')
        view_state = result['value']
        result = soup.find('input', id='__EVENTVALIDATION')
        event_validation = result['value']

        url = 'http://www.fdty.fudan.edu.cn/sportscore/default.aspx'
        data = {"__EVENTTARGET": "", "__EVENTARGUMENT": "", "__LASTFOCUS": "",
                "__VIEWSTATE": view_state, "__EVENTVALIDATION": event_validation,
                "dlljs": "st", "Button1": ""}
        self.__connect.open(url, data)

    def get_exercise(self):
        """Return the information of exercise."""
        # Login the exercise system if not.
        if not self.__exercise_is_login:
            self.__login_exercise()
            self.__exercise_is_login = True

        url = 'http://www.fdty.fudan.edu.cn/sportScore/stScore.aspx'
        content = self.__connect.open(url)
        if content is None:
            return []

        # Get the <span> with the information we want.
        soup = BeautifulSoup(content)
        result = soup.find('span', id='lblmsg')

        # Use regular expression to get the info we want.
        pattern = re.compile(ur'<td[^>]*>([^<]*)</td>')
        res_list = pattern.findall(unicode(result))
        ans = []
        for i in xrange(0, len(res_list) - 1, 2):
            ans.append((res_list[i].strip(), res_list[i + 1].strip()))

        return ans

    def get_gpa(self):
        """Return the information of scores."""
        url = 'http://www.urp.fudan.edu.cn:78/epstar/app/fudan/ScoreManger/ScoreViewer/Student/Course.jsp'
        content = self.__connect.open(url)
        if content is None:
            return []

        # Get the <tr> with the information we want.
        soup = BeautifulSoup(content)
        result = soup.find('tr', id='tr_0')

        ans = []
        while result is not None:
            course = []
            row = result.contents
            for i in xrange(1, len(row), 2):
                course.append(row[i].string.strip())
            ans.append(tuple(course))
            result = result.nextSibling.nextSibling

        return ans
