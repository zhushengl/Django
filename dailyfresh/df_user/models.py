# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    ureceiver = models.CharField(max_length=20, null=True)
    uaddress = models.CharField(max_length=100, null=True)
    upc = models.CharField(max_length=6, null=True)
    uphone = models.CharField(max_length=11, null=True)


