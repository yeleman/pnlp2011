#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, RequestContext, redirect

from pnlp_web.utils import get_level_for
from pnlp_web.views import validation
from pnlp_web.decorators import provider_required

@provider_required
def index(request):
    provider = request.user.get_profile()

    level = get_level_for(provider)

    # forward user to his matching level
    if level == 'national':
        return index_national(request)

    if level == 'region':
        return validation.validation_list(request)
        return index_region(request)

    if level == 'district':
        return validation.validation_list(request)
        return index_district(request)

    return index_norole(request)


@login_required
def index_national(request):
    context = {}
    return render(request, 'index_national.html', context)


@login_required
def index_region(request):
    context = {}
    return render(request, 'index_region.html', context)


@login_required
def index_district(request):
    context = {}
    return render(request, 'index_district.html', context)


@login_required
def index_norole(request):
    #raise Http404
    return render(request, 'index.html', {})
