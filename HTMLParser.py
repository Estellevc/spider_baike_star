from bs4 import BeautifulSoup
import re
import lxml
import urllib.parse
class HTMLParser(object):
    dict = {
        '中文名': 'chinest_name',
        '外文名': 'englist_name',
        '国籍': 'nationality',
        '民族': 'national',
        '星座':'constellation',
        '血型':'bloodtype',
        '身高':'height',
        '体重':'weight',
        '出生地':'birthplace',
        '出生日期':'birthday',
        '职业':'job',
        '毕业院校':'graduate_institutions'
    }
    def _get_new_urls_and_data(self, page_url, soup):
        res_data = {}
        new_urls = set()
        name = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
        res_data['name'] = name.get_text()
        res_data['uid'] = self.get_uid(page_url)
        res_data['data'] = [];
        res_data['profile'] = {};
        frienddiv = soup.find('div', class_="star-info-block relations")
        if frienddiv == None:
            return None, None
        #寻找个人资料
        profilediv = soup.find('dl', class_="basicInfo-block basicInfo-left")
        if profilediv is None:
            return None;
        profilelist_key = profilediv.find_all('dt', class_="basicInfo-item name")
        profilelist_value = profilediv.find_all('dd', class_="basicInfo-item value")
        #print(profilelist_key)
        if profilelist_key is None or profilelist_value is None:
            return None
        for (key,value) in zip(profilelist_key, profilelist_value):
            item_key = key.get_text().replace('\xa0','')
            item_value = value.get_text().replace('\n','')
            item_key = self.to_english(item_key)
            if item_key is None:
                continue
            res_data['profile'][item_key] = item_value

            #print(info)
        #寻找关系
        friendlist = frienddiv.find('ul', class_="slider maqueeCanvas")
        if friendlist == None:
            return None, None
        friends = friendlist.find_all('a')

        for friend in friends:
            new_url = friend['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            self.get_uid(new_full_url)
            new_urls.add(new_full_url)

            info = {}
            info['friend_name'] = friend.div['title']
            info['friend_relationship'] = friend.div.contents[0]
            info['uid'] = self.get_uid(new_full_url)
            res_data['data'].append(info)

        return new_urls, res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        # soup = BeautifulSoup(html_cont,'html.parser')
        soup = BeautifulSoup(html_cont, 'lxml')

        new_urls, new_data = self._get_new_urls_and_data(page_url, soup)
        return new_urls, new_data
    def get_uid(self,url):
        #print(url)
        if url is None:
            return;
        arr = url.split('/')
        uid = arr[len(arr)-1]
        return uid;
    def to_english(self,key):
        if key is None:
            return None
        if key in self.dict.keys():
            return self.dict[key]
        else:
            return None

