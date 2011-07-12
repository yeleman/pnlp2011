#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from pnlp_web.http import Http403
from pnlp_core.data import provider_can_or_403


def provider_required(target):
    """ Web view decorator ensuring visitor is a logged-in Provider """
    def wrapper(request, *args, **kwargs):
        try:
            web_provider = request.user.get_profile()
        except:
            # either not logged-in or non-provider user
            web_provider = None
        if web_provider:
            # user is a provider, forward to view
            return target(request, *args, **kwargs)
        else:
            # if user is logged-in (non-provider)
            # send him a message
            if request.user.is_authenticated():
                messages.error(request, _(u"The credentials you are " \
                                          "using to log in are not " \
                                          "valid. Please contact ANTIM."))
            # then foward logged-in or not to the login page.
            # logged-in users will see message there.
            return redirect('/login')
    return wrapper


def provider_permission(permission, entity=None):
    """ Web views decorator checking for premission on entity """
    def decorator(target):
        def wrapper(request, *args, **kwargs):
            try:
                web_provider = request.user.get_profile()
                assert(web_provider)
            except:
                # user is not a provider. could be logged-in though.
                # forwards to provider_required
                return provider_required(target)(request, *args, **kwargs)
            else:
                # user is valid provider.
                # need to check if has permission. if not, 403.
                if provider_can_or_403(permission, web_provider, entity):
                    return target(request, *args, **kwargs)
                raise Http403
        return wrapper
    return decorator
