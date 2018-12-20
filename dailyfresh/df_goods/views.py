# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.shortcuts import render
from models import TypeInfo, GoodsInfo


def index(request):
    typelist = TypeInfo.objects.all()

    # 查询各分类的最新4条数据
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    # 查询各分类的最热4条数据
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    context = {'title': '首页', 'type0': type0, 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4, 'type5': type5, 'type01': type01, 'type11': type11, 'type21': type21, 'type31': type31, 'type41': type41, 'type51': type51}

    return render(request, 'df_goods/index.html', context)


def list(request, tid, pindex, sort):
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    new = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    # 默认，最新
    if sort == '1':
        goods_list = typeinfo.goodsinfo_set.order_by('-id')
    # 价格
    elif sort == '2':
        goods_list = typeinfo.goodsinfo_set.order_by('-gprice')
    # 人气，点击量
    elif sort == '3':
        goods_list = typeinfo.goodsinfo_set.order_by('-gclick')
    paginator = Paginator(goods_list, 2)
    page = paginator.page(int(pindex))
    context = {'title': typeinfo.ttitle, 'page': page, 'paginator': paginator, 'typeinfo': typeinfo,'sort': sort, 'new': new}
    return render(request, 'df_goods/list.html', context)


def detail(request, id):
    goods = GoodsInfo.objects.get(id=id)
    goods.gclick = goods.gclick+1
    goods.save()
    new = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'title': goods.gtype.ttitle, 'goods': goods, 'new': new, 'id': id}
    response = render(request, 'df_goods/detail.html', context)

    # 浏览商品id组成的字符串，用来记录最新浏览，在用户中心使用
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = str(goods.id)
    # 判断是否有浏览记录，如果有则继续判断
    if goods_ids != '':
        # 将字符串拆分为列表
        goods_ids_list = goods_ids.split(',')
        # 如果商品已经被记录，则删除
        if goods_ids_list.count(goods_id) >= 1:
            goods_ids_list.remove(goods_id)
        # 添加到第一个
        goods_ids_list.insert(0, goods_id)
        # 如果超过6个则删除最后一个
        if len(goods_ids_list) >= 6:
            del goods_ids_list[5]
        # 拼接为字符串
        goods_ids = ','.join(goods_ids_list)
    else:
        # 如果没有浏览记录则直接添加
        goods_ids = goods_id
    response.set_cookie('goods_ids', goods_ids)
    return response







