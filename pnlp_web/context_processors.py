#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from pnlp_web.utils import get_level_for


def add_provider(request):
    """ Add the provider object of logged-in user or None """
    try:
        web_provider = request.user.get_profile()
    except:
        web_provider = None
    return {'web_provider': web_provider}


def add_level(request):
    """ Add level (hierachy slug) of logged-in provider or None """
    try:
        level = get_level_for(request.user.get_profile())
    except:
        level = None
    return {'level': level}
