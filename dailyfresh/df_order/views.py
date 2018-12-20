# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from df_user.models import UserInfo
from df_cart.models import CartInfo
from df_user.user_decorator import login_fun
from django.db import transaction
from models import OrderInfo, OrderDetailInfo
from datetime import datetime
from decimal import Decimal


@login_fun
def order(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    cart_ids = request.GET.getlist('cart_id')
    cart_ids1 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)
    context = {
        'title': '订单',
        'page_name': 1,
        'carts': carts,
        'user': user,
        'cart_ids': ','.join(cart_ids)
    }
    return render(request, 'df_order/place_order.html', context)


"""
事务：一旦操作失败则全部回退
1、创建订单对象
2、判断商品的库存
3、创建详单对象
4、修改商品库存
5、删除购物车
"""
@transaction.atomic()
@login_fun
def order_handle(request):
    tran_id = transaction.savepoint()
    # 接收购物车编号
    cart_ids = request.POST.get('cart_ids')
    print cart_ids
    try:
        # 创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = now.strftime('%Y%m%d%H%M%S') + str(uid)
        print order.oid
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(request.POST.get('total'))
        order.save()
        # 创建详单对象
        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids1:
            detail = OrderDetailInfo()
            detail.order = order
            # 查询购物车信息
            cart = CartInfo.objects.get(id=id1)
            goods = cart.goods
            if goods.gkucun >= cart.count:
                goods.gkucun = goods.gkucun - cart.count
                goods.save()
                # 完善详单信息
                detail.goods_id = goods.id
                detail.price = goods.gprice*cart.count
                detail.count = cart.count
                detail.save()
                cart.delete()
            else:
                # 如果库存小于购买数量
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print '=======================%s' % e
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order')
