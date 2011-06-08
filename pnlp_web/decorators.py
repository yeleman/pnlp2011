#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _, ugettext_lazy

from pnlp_web.http import Http403


def provider_required(f):
    def wrap(request, *args, **kwargs):
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
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
