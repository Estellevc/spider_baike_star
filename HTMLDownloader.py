import urllib.request
from urllib.parse import quote
import string

class HTMLDownloader(object):
    def download_html(self,url):
        if url is None:
            return;
        #print(url)
        url = quote(url,safe=string.printable)
        res = urllib.request.urlopen(url)
        #print(res)
        if res.getcode() != 200:
            return;
        return res.read()