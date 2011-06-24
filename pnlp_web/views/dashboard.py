#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext, redirect

from pnlp_web.utils import get_level_for


@login_required
def index(request):
    provider = request.user.get_profile()

    level = get_level_for(provider)

    # forward user to his matching level
    if level == 'national':
        return index_national(request)

    if level == 'region':
        return index_region(request)

    if level == 'district':
        return index_district(request)

    return index_norole(request)


@login_required
def index_national(request):
    context = {}
    return render_to_response('index_national.html', \
                              context, RequestContext(request))


@login_required
def index_region(request):
    context = {}
    return render_to_response('index_region.html', \
                              context, RequestContext(request))


@login_required
def index_district(request):
    context = {}
    return render_to_response('index_district.html', \
                              context, RequestContext(request))


@login_required
def index_norole(request):
    #raise Http404
    return render_to_response('index.html', {}, RequestContext(request))
