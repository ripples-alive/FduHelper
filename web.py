#!/usr/bin/python
#encoding:utf-8

import urllib
import urllib2
import cookielib

class Web:
    def __init__(self, loginUrl, data):
        self.__login(loginUrl, data)

    def __login(self, loginUrl, data):
        try:
            cj = cookielib.CookieJar()
            self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            self.__opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
            self.__opener.open(loginUrl, urllib.urlencode(data))

        except Exception, e:
            print e

    def logout(self, logoutUrl):
        try:
            self.__opener.open(logoutUrl)
        except Exception, e:
            print e

    def open(self, url, data=None, method='POST'):
        try:
            if method == 'POST':
                if (data == None):
                    return self.__opener.open(url).read()
                else:
                    return self.__opener.open(url, urllib.urlencode(data)).read()
            elif method == 'GET':
                return self.__opener.open(url + '?' + urllib.urlencode(data)).read()
        except Exception, e:
            print e
