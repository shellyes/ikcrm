#coding:utf-8
import requests
from lxml import etree

rs = requests.session()
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}
url = 'https://www.ikcrm.com/users/sign_in'

origin_data = rs.get(url=url, headers=headers)
data = etree.HTML(origin_data.content)

authenticity_token = data.xpath('//input[@name="authenticity_token"]/@value')[0]




login_data = {'authenticity_token':authenticity_token,
                'user[login]':'18180428128',
                'user[password]':'kalibei1228',
                'user[remember_login]':0,
                'commit': '登录'
                }

loin = rs.post(url, data=login_data, headers=headers)

pageurl = 'https://e.ikcrm.com/opportunities?page=3&per_page=50&scope=all_own&type=advance&section_only=true'
page_data = rs.get(url=pageurl, headers=headers)
# print page_data.content
