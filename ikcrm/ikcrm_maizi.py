#coding:utf-8
import requests
import json
import time
from datetime import datetime
import math
import sys
import traceback

"""
    global_parameter  全局参数,请求所有的url都必须使用。
    headers   请求头
"""

#登录函数
def login():
    global global_parameter
    global headers

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    url = "https://api.ikcrm.com/api/v2/auth/login"
    login_data = {'login': '18180428128', 'password': 'kalibei1228', 'device': "dingtalk"}
    json_data = requests.post(url=url, json=login_data, headers=headers).content

    # 获取全局参数
    user_token = json.loads(json_data)['data']['user_token']
    global_parameter = 'user_token=' + user_token + '&device=dingtalk&version_code=3.13.0'

    print '登录返回数据', json.loads(json_data)


#获取商机分页数
def get_opportunities_page(stage, per_page):
    # 获取商机总条数
    opportunities_url = 'https://api.ikcrm.com/api/v2/opportunities?stage='+str(stage)+'&' + global_parameter
    opportunities_data = requests.get(url=opportunities_url, headers=headers).content
    total_count = json.loads(opportunities_data)['data']['total_count']
    total_page = int(math.ceil(total_count / float(per_page)))

    print '商机总条数：', total_count, '总页数', total_page

    return total_page

# 客户调入公海函数
def rm_common(customer_id, common_id):

    rm_url = 'https://api.ikcrm.com/api/v2/customers/'+str(customer_id)+'/turn_common?common_id='+str(common_id)+'&'+global_parameter
    rm_data = requests.put(url=rm_url, headers=headers).content
    rm_json = json.loads(rm_data)['data']

    print '客户调入公海',json.dumps(rm_json)


#写入要移动客户信息函数
def file_operate(customer_info, time_info, revisit_info, rm_info):
    septal_line = '-----------------------------------------------------------------\n'
    with open('info.log', 'a') as f:
        f.write(septal_line)
        f.write(customer_info)
        f.write(time_info)
        f.write(revisit_info)
        f.write(rm_info)
        f.write(septal_line)



'''
联系中stage=1129592
新数据(第一阶段): #创建时间进行比较
03小时未跟进         掉入"事故公海池-3小时未跟" common_id='11629'
18小时跟进次数少于2次  掉入"事故公海池-未3天5打" common_id='12028'
72小时跟进次数少于5次  掉入"事故公海池-未3天5打" common_id='12028'

新老数据(第一阶段): #跟进时间进行比较
72小时未跟进  掉入"事故公海池-1阶段3天未跟" common_id='11628'
'''

def feach_new_data(per_page):
    #获取商机总条数
    total_page = get_opportunities_page(stage='1129692', per_page=50)

    for page in range(1, total_page+1):
        print '筛选第'+str(page)+'页信息'

        #根据页获取所有商机里的信息列表。
        opportunities_url = 'https://api.ikcrm.com/api/v2/opportunities?stage=1129692&per_page='+str(per_page)+'&page='+str(page)+'&'+global_parameter
        opportunities_data = requests.get(url=opportunities_url, headers=headers).content
        all_opportunities = json.loads(opportunities_data)['data']['opportunities']

        for opportunities in all_opportunities:
            revisit_time = opportunities['real_revisit_at']
            created_time = opportunities["created_at"]
            opportunities_id = opportunities['id']
            title = opportunities['title']
            customer_name = opportunities['customer_name']
            customer_id = opportunities["customer_id"]

            #时间处理,转化为datatime类型
            revisit_time = datetime.strptime(revisit_time, '%Y-%m-%d %H:%M')
            created_time = datetime.strptime(created_time, '%Y-%m-%d %H:%M')

            start_time = datetime(2017, 8, 1, 0, 0, 0)
            now_time = datetime.now()

            #只对2017.8.1日后的数据进行操作。
            if (created_time-start_time).days >= 0:

                # 某条商机跟进记录，获取跟进记录条数。
                time.sleep(1)
                revisit_detail_url = 'https://api.ikcrm.com/api/v2/revisit_logs/new_index?loggable_type=opportunity&loggable_id=' + str(
                    opportunities_id) + '&' + global_parameter
                revisit_detail_data = requests.get(url=revisit_detail_url, headers=headers).content
                revisit_count = json.loads(revisit_detail_data)['data']['total_count']

                time.sleep(1)
                #商机详情，获取befor_user是否存在，判定是否发生了复制人是否发生了转移
                opportunities_detail_url = 'https://api.ikcrm.com/api/v2/opportunities/' + str(opportunities_id) + '?' + global_parameter
                opportunities_detail_data = requests.get(url=opportunities_detail_url, headers=headers).content
                first_opportunities = json.loads(opportunities_detail_data)['data']
                # print '商机详情：', json.dumps(first_opportunities)

                before_user = first_opportunities['customer']['before_user']

                # 新数据跟进判定
                if (revisit_count!=0 and len(before_user) !=0 ):
                    print '客户发生了转移', customer_name,'商机id', opportunities_id
                    created_time = json.loads(revisit_detail_data)['data']['revisit_logs'][::-1][0]['created_at']
                    created_time = datetime.strptime(created_time, '%Y-%m-%d %H:%M')
                    time_hours = (now_time - created_time).seconds / 3600
                    time_days = (now_time - created_time).days
                else:
                    time_hours = (now_time - created_time).seconds / 3600
                    time_days = (now_time - created_time).days


                # 新旧数据判定
                time_hours_r = (now_time - revisit_time).seconds / 3600
                time_days_r = (now_time - revisit_time).days



                print  time_days,time_hours,revisit_count
                if time_days == 0 and 3 <= time_hours < 4.5 and revisit_count == 0:

                    # info信息写入info.log
                    customer_info = '课程:%s 客户:%s(第%s页) 商机：%s\n'% (title.encode('utf-8'),customer_name.encode('utf-8'),str(page),opportunities_id)
                    time_info = '创建时间：%s 跟进时间：%s 当前时间：%s\n' % (created_time,revisit_time,(now_time))
                    revisit_info = '跟进状况：%s天%s小时未跟进 跟进条数：%s\n'% (time_days, time_hours, revisit_count)
                    rm_info = '操作：掉入<事故-新建3小时未跟>\n'
                    file_operate(customer_info, time_info, revisit_info, rm_info)

                    # 客户移入3小时未跟
                    # rm_common(customer_id, 11629)

                elif time_days == 0 and 18 <= time_hours < 19.5 and revisit_count < 2:

                    #info信息写入info.log
                    customer_info = '课程:%s 客户:%s(第%s页) 商机：%s\n' % (title.encode('utf-8'), customer_name.encode('utf-8'), str(page),opportunities_id)
                    time_info = '创建时间：%s 跟进时间：%s 当前时间：%s\n' % (created_time, revisit_time, (now_time))
                    revisit_info = '跟进状况：%s天%s小时未跟进 跟进条数：%s\n' % (time_days, time_hours, revisit_count)
                    rm_info = '操作：掉入<事故-未3天5打> 18小时内小于两条\n'
                    file_operate(customer_info, time_info, revisit_info, rm_info)

                    #客户移入3天5打
                    # rm_common(customer_id, 12028)

                elif time_days >= 3 and time_hours > 0 and revisit_count < 5:

                    # info信息写入info.log
                    customer_info = '课程:%s 客户:%s(第%s页) 商机：%s\n' % (title.encode('utf-8'), customer_name.encode('utf-8'), str(page),opportunities_id)
                    time_info = '创建时间：%s 跟进时间：%s 当前时间：%s\n' % (created_time, revisit_time, (now_time))
                    revisit_info = '跟进状况：%s天%s小时未跟进 跟进条数：%s\n' % (time_days, time_hours, revisit_count)
                    rm_info = '操作：掉入<事故-未3天5打> 72小时内小于五条\n'
                    file_operate(customer_info, time_info, revisit_info, rm_info)

                    #客户移入3天5打
                    # rm_common(customer_id, 12028)

                if time_days_r >= 3 and time_hours_r > 0:

                    # info信息写入info.log
                    customer_info = '课程:%s 客户:%s(第%s页) 商机：%s\n' % (title.encode('utf-8'), customer_name.encode('utf-8'), str(page),opportunities_id)
                    time_info = '创建时间：%s 跟进时间：%s 当前时间：%s\n' % (created_time, revisit_time, (now_time))
                    revisit_info = '跟进状况：%s天%s小时未跟进 跟进条数：%s\n' % (time_days_r, time_hours_r, revisit_count)
                    rm_info = '操作：掉入<事故-1阶段3天未跟>\n'
                    file_operate(customer_info, time_info, revisit_info, rm_info)

                    #客户移入3天未跟进
                    # rm_common(customer_id, 11628)


'''
输单数据: #更新时间进行比较
输单stage=1129697
12小时后掉入oc输单公海 common_id='11637'

'''

def fetch_lose_data():
    #获取输单商机总条数
    total_page = get_opportunities_page(stage='1129697', per_page=50)

    for page in range(1, total_page+1):
        print '筛选第'+str(page)+'页信息'
        time.sleep(2.0)
        opportunities_url = 'https://api.ikcrm.com/api/v2/opportunities?stage=1129697&per_page=50'+'&page='+str(page)+'&'+global_parameter
        opportunities_data = requests.get(url=opportunities_url, headers=headers).content
        all_opportunities = json.loads(opportunities_data)['data']['opportunities']


        for opportunities in all_opportunities:
            revisit_time = opportunities['real_revisit_at']
            customer_id = opportunities["customer_id"]
            customer_name = opportunities['customer_name']
            title =opportunities['title']


            revisit_time = datetime.strptime(revisit_time, '%Y-%m-%d %H:%M')
            start_time = datetime(2017, 8, 1, 0, 0, 0)
            now_time = datetime.now()

            time_lose_hours = (now_time - revisit_time).seconds/3600
            time_lose_days = (now_time - revisit_time).days


            if (revisit_time-start_time).days >= 0:
                if (time_lose_days == 0 and time_lose_hours > 12) or time_lose_days > 1:
                    # info信息写入info.log
                    customer_info = '课程:%s 客户:%s(第%s页)\n' % (title.encode('utf-8'), customer_name.encode('utf-8'), str(page))
                    time_info = '跟进时间：%s 当前时间：%s \n' % (revisit_time, (now_time))
                    revisit_info = '跟进状况：%s天%s小时未跟进\n' % (time_lose_days,time_lose_hours)
                    rm_info = '操作：掉入<OC-输单>\n'
                    file_operate(customer_info, time_info, revisit_info, rm_info)

                    #客户移入输单
                    # rm_common(customer_id, 11637)


#程序异常邮件发送给管理员。
def send_mail(receivers, theme, content):
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = theme  #邮件主题
    msg['From'] = sender    #发件人
    msg['To'] = receivers #收件人
    # msg['To'] = ";".join(receivers)  #将收件人列表以分号分隔

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  #连接邮箱服务器，默认端口25
        server.login(mail_user, mail_pass)  #登录邮箱
        server.sendmail(sender, receivers, msg.as_string())  #发送邮件SMTP.sendmail(from_addr, to_addrs, msg[, mail_options, rcpt_options]
        server.close()

        email_status = {'status': True, 'content': '发送消息成功'}
        return email_status

    except Exception as e:
        email_status = {'status': False, 'content': '发送消息成失败,错误详情%s' % str(e)}
        return email_status

def run():
    start_time = datetime.now()
    login()
    feach_new_data(50)
    time.sleep(1.0)
    fetch_lose_data()
    end_time = datetime.now()
    print end_time - start_time
    time.sleep(3600)

if __name__ == '__main__':

    mail_host = "smtp.163.com"  # 使用的邮箱的smtp服务器地址
    mail_user = "thoftheocean@163.com"  # 发件人昵称
    mail_pass = "wy151932"  # 密码
    receivers = 'thoftheocean@gmail.com'  # 收件人邮箱
    sender = 'thoftheocean@163.com' #发件人

    while True:
        try:
            with open('info.log','a') as f:
                f.truncate()
            run()
        except Exception as e:
            error_log = str(sys.exc_info()[0]) + str(sys.exc_info()[1])
            print '程序异常已经暂停服务！错误状况邮件已经发送给管理员'

            # #发送邮件
            # email_info = '错误类型已经原因：' + error_log + '\n详情请查看错误日志文件'
            # email_status = send_mail(receivers, "ikcrm二次开发程序错误邮件", email_info )
            # if email_status['status']:
            #     print email_status['content']
            # else:
            #     print email_status['content']

            # 添加错误日志
            with open('error.log', 'a') as f:
                f.truncate()
                f.write('error time:%s\n' % datetime.now())
                traceback.print_exc(file=f)
                f.write('-------------------------------------------------------------\n')

            #处理网络异常问题,延时10分钟后进行请求。
            run()





