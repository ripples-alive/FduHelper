#!/usr/bin/python
#encoding:utf-8

import urllib
import urllib2
import cookielib


class Web:
    """Class to open URLs with cookies."""

    def __init__(self, login_url, data):
        """Init with given URL and post data."""
        self.__login(login_url, data)

    def __login(self, login_url, data):
        """Login with given URL and post data."""
        try:
            # Create opener with cookie jar and update the headers.
            cj = cookielib.CookieJar()
            self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            self.__opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
            self.__opener.open(login_url, urllib.urlencode(data))

        except Exception, e:
            print e

    def logout(self, logout_url):
        """Logout with given URL."""
        try:
            self.__opener.open(logout_url)
        except Exception, e:
            print e

    def open(self, url, data=None, method='POST'):
        """Return string for the specified URL."""
        try:
            if method == 'POST':
                if data is None:
                    return self.__opener.open(url).read()
                else:
                    return self.__opener.open(url, urllib.urlencode(data)).read()
            elif method == 'GET':
                return self.__opener.open(url + '?' + urllib.urlencode(data)).read()
        except Exception, e:
            print e
