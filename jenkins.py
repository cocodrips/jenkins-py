import urllib2
import base64
import os

from xml.etree import ElementTree

class Jenkins(object):
    def __init__(self, jenkins_url, user="", passwd=""):
        self.base_url = jenkins_url
        self.user = user
        self.passwd = passwd

    def get(self, path):
        """
        Access jenkins api

        :param path: http://<jenkins:url>/<path>
        :return: string
        """
        url = os.path.join(self.base_url, path)
        print url
        proxy = urllib2.ProxyHandler({
            'http': url
        })

        opener = urllib2.build_opener(proxy)
        authstr = '{0}:{1}'.format(self.user, self.passwd)
        base64string = base64.encodestring(authstr).replace('\n', '')
        opener.addheaders = [ ("Authorization", "Basic {0}".format(base64string)) ]
        conn = opener.open(url)
        return conn.read()

    def get_job_config(self, jobname):
        """
        :param jobname: string
        :return: xml.etree.ElementTree.Element
        """
        path = 'job/{}/config.xml'.format(jobname)
        res = self.get(path)
        return ElementTree.fromstring(res)

if __name__ == '__main__':
    j = Jenkins('http://localhost:8080/', 'hoge', 'hoge')
    print j.get('api/json')
    print j.get_job_config('test')