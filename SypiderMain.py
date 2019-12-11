
import HTMLParser
import HTMLDownloader
import UrlManager
from py2neo import Graph,Node,Relationship,NodeMatcher
class SpiderMain(object):
    def __init__(self):
        #连接neo4j数据库
        self.graph = Graph('http://localhost:7474', username='neo4j', password='123456')
        self.matcher = NodeMatcher(self.graph)
        self.url_manger = UrlManager.UrlManager()
        self.html_downloader = HTMLDownloader.HTMLDownloader()
        self.html_parser = HTMLParser.HTMLParser()
    def spider(self,root_url):
        #print(root_url)
        count = 0
        self.url_manger.add(root_url)
        while self.url_manger.has_new():
            try:
                new_url = self.url_manger.get_new()
                print(count)
                print(new_url)
                html = self.html_downloader.download_html(new_url)
                new_urls,new_date = self.html_parser.parse(new_url, html)
                #print(new_date)
                #print(new_urls)
                #查找该节点是否已经存在
                if new_date is None:
                    continue
                if new_urls is None:
                    continue
                nodes_res = self.graph.nodes.match("baikestar",uid=new_date['uid'])
                nodes_res_list = list(nodes_res)

                if len(nodes_res_list) == 0:
                    node1 = Node('baikestar',name=new_date['name'],uid=new_date['uid'],**new_date['profile'])
                    self.graph.create(node1)
                else:
                    node1 = nodes_res_list[0]

                if len(new_date['data']) > 0:
                    for item in new_date['data']:
                        sub_res = self.graph.nodes.match("baikestar",uid=item['uid'])
                        sub_res_list = list(sub_res)
                        if len(sub_res_list) == 0:
                            node2 = Node('baikestar',name=item['friend_name'],uid=item['uid'])
                        else:
                            node2 = sub_res_list[0]
                        r = Relationship(node1, item['friend_relationship'], node2)
                        self.graph.create(r)
                self.url_manger.add_url_list(new_urls)
                if count == 1000:
                    break
                count += 1
            except Exception as e:
                print('crawl failed', e)
            print('结束')
if __name__ == "__main__":
    root_url = "https://baike.baidu.com/item/胡歌/312718"
    spider = SpiderMain()
    spider.spider(root_url)