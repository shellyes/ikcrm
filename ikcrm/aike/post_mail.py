#! /usr/bin/env python
#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.163.com"  # 使用的邮箱的smtp服务器地址
mail_user = "thoftheocean@163.com"  # 发件人昵称
mail_pass = "wy151932"  # 密码

# receivers = ['1848500475@qq.com']     #收件邮箱(列表)
receivers = 'thoftheocean@gmail.com'
sender = 'thoftheocean@163.com'  # 发件人邮箱

#程序异常邮件发送给管理员。
def send_mail(receivers, theme, content):
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = theme  #邮件主题
    msg['From'] = sender    #发件人
    msg['To'] = receivers   #收件人
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
        email_status = {'status': False, 'content': '发送消息成失败%,错误详情%s' % str(e)}
        return email_status



if __name__ == '__main__':
    #是否解码看具体情况。
    result = send_mail(receivers, "ikcrm程序错误邮件", 'ikrm出错咯，赶快派攻城狮去维护')
    if result:
        print '发送邮件成功'
    else:
        print '发送邮件失败'

