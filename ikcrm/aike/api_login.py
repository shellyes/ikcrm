#coding:utf-8
import requests
import json

rs = requests.session()
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

# headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

#方法一: 直接加参数传过去,不考虑数据类型:
# url = "https://api.ikcrm.com/api/v2/auth/login?login=18180428128&password=kalibei1228&device=dingtalk"

#方法二: json格式的数据,所以要对数据进行转换为json数据data=json.dumps(login_data)或者直接jion=login_data。
url = "https://api.ikcrm.com/api/v2/auth/login"

login_data = {'login': '18180428128', 'password': 'kalibei1228', 'device': "dingtalk"}

json_data = rs.post(url=url, json=login_data, headers=headers).content

#转换为字典形式
dict_data = json.loads(json_data)


required_parameter={}
required_parameter['user_token'] = dict_data['data']['user_token']
required_parameter['version_code'] = '3.13.0'
required_parameter['device'] = 'dingtalk_open'
print required_parameter
