#coding:utf-8
import requests
import json

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

# headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

#方法一: 直接加参数传过去,不考虑数据类型:
# url = "https://api.ikcrm.com/api/v2/auth/login?login=18180428128&password=kalibei1228&device=dingtalk"

#方法二: json格式的数据,所以要对数据进行转换为json数据data=json.dumps(login_data)或者直接jion=login_data。
url = "https://api.ikcrm.com/api/v2/auth/login"

login_data = {'login': '18180428128', 'password': 'kalibei1228', 'device': "dingtalk"}

json_data = requests.post(url=url, json=login_data, headers=headers).content

#转换为字典形式
dict_data = json.loads(json_data)

print dict_data


user_id = dict_data['data']['user_id']
user_token = dict_data['data']['user_token']
version_code = '3.13.0'
device = 'dingtalk_open'


globals_p = 'user_token='+str(dict_data['data']['user_token'])+'&device=dingtalk&version_code=3.13.0'

#------------------------商机---------------------------------



# opportunities_url = 'https://api.ikcrm.com/api/v2/opportunities?stage=1129692&per_page=50&page=1&'+globals_p
# opportunities_data = requests.get(url=opportunities_url, headers=headers).content
# first_opportunities = json.loads(opportunities_data)['data']['opportunities']
# opportunities_id = first_opportunities
#
# # print 'customers_id:', opportunities_id
# print '页第一分商机',json.dumps(first_opportunities)


# opportunities_detail_url = 'https://api.ikcrm.com/api/v2/opportunities/164406'+'?' + globals_p
# opportunities_detail_data = requests.get(url=opportunities_detail_url, headers=headers).content
# first_opportunities = json.loads(opportunities_detail_data)['data']
#
# print '商机详情：', json.dumps(first_opportunities)


# #--------------------------商机排序----------------------------------
# opportunities_sort_url = 'https://api.ikcrm.com/api/v2/opportunities?page=1&sort=real_revisit_at&order=desc&'+globals_p
# opportunities_sort_data = requests.get(url=opportunities_sort_url, headers=headers).content
# first_sort_opportunities = json.loads(opportunities_sort_data)
#
# print '总的条数',first_sort_opportunities['data']['total_count']
# print '第一页的商机', json.dumps( first_sort_opportunities['data']['opportunities'])
#


#------------------------商机筛选--------------------------------------
#
# # 商机筛选分组/api/v2/opportunities/filter_sort_group(.:format)
# opportunities_filters_url = 'https://api.ikcrm.com/api/v2/opportunities/filter_sort_group?'+globals_p
# opportunities_filters_data = requests.get(url=opportunities_filters_url, headers=headers).content
#
# print '商机销售状态进行筛选：', opportunities_filters_data
#
#
# #销售状态/api/v2/opportunities/:field_name/filter_options(.:format)
# opportunities_filter_url = 'https://api.ikcrm.com/api/v2/opportunities/stage/filter_options?'+globals_p
# opportunities_filter_data = requests.get(url=opportunities_filter_url, headers=headers).content
# first_filter_opportunities = json.loads(opportunities_filter_data)['data']
#
# print '商机状态进行筛选：', json.dumps(first_filter_opportunities)

#
# opportunities_filter_url ='https://api.ikcrm.com/api/v2/opportunities?stage=1129697&'+ globals_p
# opportunities_filter_data = requests.get(url=opportunities_filter_url, headers=headers).content
# first_filter_opportunities = json.loads(opportunities_filter_data)['data']
#
# print '输单数据：', json.dumps(first_filter_opportunities)
#





#--------------------------------客户-------------------------

#
# customers_url = 'https://api.ikcrm.com/api/v2/customers?per_page=50&page=1&'+globals_p
# customers_data = requests.get(url=customers_url, headers=headers).content
#
# first_customers = json.loads(customers_data)['data']['customers'][0]
# customers_id = first_customers['id']
#
# print '101页第一个位客户',json.dumps(first_customers)


# customers_detail_url = 'https://api.ikcrm.com/api/v2/customers/'+'3670520'+'?'+globals_p
# customers_detail_data = requests.get(url=customers_detail_url, headers=headers).content
#
# customers_json = json.loads(customers_detail_data)
#
# print '客户详情', json.dumps(customers_json)


#--------------------------跟进记录------------------------------------------


# revisit_url = 'https://api.ikcrm.com/api/v2/revisit_logs/new_index?per_page=20&stage=1129692&'+globals_p
# revisit_data = requests.get(url=revisit_url, headers=headers).content
# revisit_json = json.loads(revisit_data)
#
# print '跟进记录详情', json.dumps(revisit_json)
# #
# #
revisit_detail_url = 'https://api.ikcrm.com/api/v2/revisit_logs/new_index?loggable_type=opportunity&loggable_id='+'154789'+'&'+globals_p
revisit_detail_data = requests.get(url=revisit_detail_url, headers=headers).content
revisit_detail_json = json.loads(revisit_detail_data)

print '某条商机跟进记录详情', json.dumps(revisit_detail_json)


#-------------------------客户转移到公海------------------------------------


#客户转移:PUT /api/v2/customers/:id/turn_common?common_id=:common_id  移送到oc输单
# rm_url = 'https://api.ikcrm.com/api/v2/customers/'+'3666598'+'/turn_common?common_id=11637&'+globals_p
# rm_data = requests.put(url=rm_url, headers=headers).content
# rm_json = json.loads(rm_data)['data']
#
# print '客户调入公海',json.dumps(rm_json)

#公海类型
# rm_url = 'https://api.ikcrm.com/api/v2/common_customers/common_settings?'+globals_p
# rm_data = requests.get(url=rm_url, headers=headers).content
# rm_json = json.loads(rm_data)['data']
#
# print '客户调入公海',json.dumps(rm_json)



