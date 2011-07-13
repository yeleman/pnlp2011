#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.conf import settings

from pnlp_web.utils import get_level_for, random_proverb


def add_provider(request):
    """ Add the provider object of logged-in user or None """
    try:
        web_provider = request.user.get_profile()
    except:
        web_provider = None

    fortune = random_proverb() if settings.ENABLE_FORTUNE else None
    return {'web_provider': web_provider, 'fortune': fortune}


def add_level(request):
    """ Add level (hierachy slug) of logged-in provider or None """
    try:
        level = get_level_for(request.user.get_profile())
    except:
        level = None
    return {'level': level}
