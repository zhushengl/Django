# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect


def login_fun(func):
    def wrapper(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)

        else:
            response = HttpResponseRedirect('/user/login')
            response.set_cookie('url', request.get_full_path())
            return response
    return wrapper



def login_fun(func):
    def wrapper(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            response = HttpResponseRedirect('/user/login')
            response.set_cookie('url', request.get_full_path())
            return response
        return wrapper()