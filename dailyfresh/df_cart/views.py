# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse
from models import CartInfo
from df_user.user_decorator import login_fun


# 购物车显示商品数量
@login_fun
def count_num(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    counts = len(carts)
    return JsonResponse({'counts': counts})


# 购物车页
@login_fun
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    cart_ids = ''
    for cart in carts:
        cart_ids += 'cart_id=' + str(cart.id) + '&'
    context = {'title': '购物车', 'page_name': 1, 'carts': carts, 'cart_ids': cart_ids}
    return render(request, 'df_cart/cart.html', context)


# 加入购物车
@login_fun
def add(request, gid, counts):
    uid = request.session['user_id']
    gid = int(gid)
    counts = int(counts)
    # 查询购物车中是否已经有此商品，如果有则数量增加，没有则新增
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count += counts
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = counts
    cart.save()
    # 如果是ajax请求则返回json, 否则转向购物车
    if request.is_ajax():
        carts = CartInfo.objects.filter(user_id=uid)
        counts = len(carts)
        return JsonResponse({'counts': counts})
    else:
        return redirect('/cart/')


@login_fun
def edit(request, cart_id, count):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        count1 = cart.count = int(count)
        cart.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': count1}
    return JsonResponse(data)

@login_fun
def delete(request, cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)
