#!/usr/bin/python
#encoding:utf-8

import urllib
import urllib2
import cookielib

class Web:
    def __init__(self):
        self.__logined = False

    def login(self, loginUrl, data):
        try:
            cj = cookielib.CookieJar()
            self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            self.__opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
            self.__opener.open(loginUrl, urllib.urlencode(data))

            self.__logined = True
        except Exception, e:
            print str(e)

    def open(self, url, data=None):
        if self.__logined == False:
            print "Please login first!"
            return

        if (data == None):
            return self.__opener.open(url).read()
        else:
            return self.__opener.open(url, urllib.urlencode(data)).read()
