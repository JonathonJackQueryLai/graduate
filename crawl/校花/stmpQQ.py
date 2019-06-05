import random
import smtplib
from email.header import Header
from email.mime.text import MIMEText

'''
    return: 轰炸：1478817415
            试验：290104891


'''


# 产生验证码
def createVC():
    # 大小写
    def trans_ch():
        if random.sample([0, 1], 1)[0] == 1:
            ch = chr(random.randint(97, 123)).upper()
        else:
            ch = chr(random.randint(97, 123))
        return ch

    randStr = str(random.randint(0, 9)) + trans_ch() + str(random.randint(0, 9)) + trans_ch()
    return randStr


# 发送验证码
def sentEmail_QQ():
    '''
    :return:
    '''
    message = MIMEText(createVC())  # 邮件内容
    message['From'] = Header('乌鸦')  # 邮件发送者名字
    message['To'] = Header('用户')  # 邮件接收者名字
    # message['Subject'] = Header('验证码')  # 邮件主题
    # message['Subject'] = Header('验证码')  # 邮件主题
    # 'kcxoavijucmlhhbh'
    # #  'wmnmguyrpuisbecf'
    mail = smtplib.SMTP()
    mail.connect("smtp.qq.com")  # 连接 qq 邮箱
    mail.login("1614582143@qq.com", "ksigeljvbwvqeieh")  # 账号和授权码
    # mail.login("1149476001@qq.com", "kcxoavijucmlhhbh")  # 账号和授权码
    count = 0

    # '"937694839@qq.com","495900511@qq.com",'"290104891@qq.com",
    mail.sendmail("1614582143@qq.com", ["272357355@qq.com"], message.as_string())  # 发送账号、接收账号和邮件信息

    print('sent e-mail finish')


# 检验验证码是否正确
def testVC(cVC='', tVC=''):
    if cVC.__sizeof__() == 4:
        if cVC[0].lower() == tVC[0].lower() and cVC[1] == tVC[1] and cVC[2].lower() == tVC[2].lower() and cVC[3] == tVC[
            3]:
            return True
        else:
            return False
