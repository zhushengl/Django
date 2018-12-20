# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import UserInfo
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect
from user_decorator import login_fun
from df_goods.models import GoodsInfo


# 注册页面
def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    uname = request.POST.get("user_name")
    upwd = request.POST.get("pwd")
    upwd2 = request.POST.get("cpwd")
    uemail = request.POST.get("email")

    if upwd != upwd2:
        return redirect('/user/register/')

    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()

    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


# 登录页面
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    uname = request.POST.get('username')
    upwd = request.POST.get('pwd')
    urem = request.POST.get('remember')

    user = UserInfo.objects.filter(uname=uname)

    if len(user)==1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == user[0].upwd:
            url = request.COOKIES.get('url', '/')
            response = HttpResponseRedirect(url)
            # 记住用户名
            if urem != 0:
                response.set_cookie('uname', uname)
            else:
                # 设置cookie立刻过期
                response.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            return response
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname':uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname':uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


# 用户中心-个人信息
@login_fun
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_list = []
    if goods_ids == '':
        goods_list = []
    else:
        goods_ids_list = goods_ids.split(',')
        for goods_id in goods_ids_list:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title': '用户中心', 'user_name': request.session['user_name'], 'user_email': user_email, 'goods_list': goods_list}
    return render(request, 'df_user/user_center_info.html', context)


# 用户中心-全部订单
@login_fun
def order(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    orders = user.orderinfo_set.all()
    context = {'title': '用户中心', 'orders': orders}
    return render(request, 'df_user/user_center_order.html', context)


# 用户中心-收货地址
@login_fun
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        user.ureceiver = request.POST.get('ureceiver')
        user.uaddress = request.POST.get('uaddress')
        user.upc = request.POST.get('upc')
        user.uphone = request.POST.get('uphone')
        user.save()
    if user.ureceiver==None:
        user=''
    context = {'title': '用户中心', 'user': user}
    return render(request, 'df_user/user_center_site.html', context)

