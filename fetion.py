#!/usr/bin/python
#encoding:utf-8

import urllib
import urllib2
import json

class Fetion:
    def __init__(self, fromTel, password):
        self.__fromTel = fromTel
        self.__password = password

    def __getData(self, toTel, msg):
        return urllib.urlencode({'u' : self.__fromTel, 'p' : self.__password, \
            'to' : toTel, 'm' : msg})
        # return 'https://quanapi.sinaapp.com/fetion.php?u=%s&p=%s&to=%s&m=%s' \
            # %(self.__fromTel, self.__password, toTel, urllib.quote(msg))

    def sendMsg(self, msg, toTel=None):
        url = 'https://quanapi.sinaapp.com/fetion.php'
        if toTel == None:
            data = self.__getData(self.__fromTel, msg)
        else:
            data = self.__getData(toTel, msg)
        # print data

        try:
            result = urllib2.urlopen(url, data).read()
            resDict = json.loads(result)
            if resDict['result'] == 0:
                print 'Send message successfully!'
                return True
            else:
                print 'Send message failed.'
                return False
        except Exception, e:
            print e