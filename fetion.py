#!/usr/bin/python
#encoding:utf-8

import urllib
import urllib2
import json


class Fetion:
    """Class to send message by fetion."""

    def __init__(self, from_tel, password):
        self.__from_tel = from_tel
        self.__password = password

    def __get_data(self, to_tel, msg):
        return urllib.urlencode({'u': self.__from_tel, 'p': self.__password,
                                 'to': to_tel, 'm': msg})
        # return 'https://quanapi.sinaapp.com/fetion.php?u=%s&p=%s&to=%s&m=%s' \
        # %(self.__from_tel, self.__password, to_tel, urllib.quote(msg))

    def send_msg(self, msg, to_tel=None):
        """Send message to certain one.
        Send message to the user self if to_tel is omitted.
        """
        url = 'https://quanapi.sinaapp.com/fetion.php'
        if to_tel is None:
            data = self.__get_data(self.__from_tel, msg)
        else:
            data = self.__get_data(to_tel, msg)
        # print data

        try:
            # Try to send message and return the status of sending.
            result = urllib2.urlopen(url, data).read()
            res_dict = json.loads(result)
            if res_dict['result'] == 0:
                print 'Send message successfully!'
                return True
            else:
                print 'Send message failed.'
                return False
        except Exception, e:
            print e