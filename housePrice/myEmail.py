#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/3 15:45
# @Author  : @乌鸦坐飞机
# Description   :
from django.conf import settings

from_email = settings.DEFAULT_FROM_EMAIL
from django.core.mail import send_mass_mail
from django.core.mail import send_mail

send_mail('Subject here', '五一快乐', '948666249@qq.com',
          ['1027197858@qq.com'], fail_silently=False)

# send_mass_mail((message1, message2), fail_silently=False)
