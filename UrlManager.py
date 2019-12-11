import re
from urllib.parse import unquote
class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add(self,url):
        if url is None:
            return
        if re.match("http",url) and re.match("https",url) == False:
            url = re.sub("http","https",url)
        url = unquote(url)
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
    def add_url_list(self,urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add(url)
    def has_new(self):
        return len(self.new_urls)!=0
    def get_new(self):
        new_url = self.new_urls.pop();
        self.old_urls.add(new_url)
        return new_url
