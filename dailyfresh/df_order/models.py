# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('df_user.UserInfo')
    odate = models.DateTimeField(auto_now=True)
    oIsPay = models.BooleanField(default=False)
    oddress = models.CharField(max_length=100)
    ototal = models.DecimalField(max_digits=6, decimal_places=2)


class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo')
    order = models.ForeignKey(OrderInfo)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField()


