# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import TypeInfo, GoodsInfo


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'gtitle', 'gprice', 'gunit', 'gclick', 'gkucun']

admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
