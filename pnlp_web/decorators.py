#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _, ugettext_lazy

from pnlp_web.http import Http403
from pnlp_core.data import provider_can_or_403


def provider_required(f):
    def wrapped(request, *args, **kwargs):
            try:
                web_provider = request.user.get_profile()
            except:
                web_provider = None
            if web_provider:
                return f(request, *args, **kwargs)
            else:
                if request.user.is_authenticated():
                    messages.error(request, _(u"The credentials you are " \
                                              "using to log in are not " \
                                              "valid. Please contact ANTIM."))
                return redirect('/login')
    wrapped.__doc__ = f.__doc__
    wrapped.__name__ = f.__name__
    return wrapped


def provider_permission(permission, entity=None):
    def inner_perm(f):
        def wrapped(request, *args, **kwargs):
                try:
                    web_provider = request.user.get_profile()
                    assert(web_provider, True)
                except:
                    return provider_required(f)
                else:
                    if provider_can_or_403(permission, web_provider, entity):
                        return f(request, *args, **kwargs)
                    raise Http403
        return wraps(f)(wrapped)
    return inner_perm
