#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, RequestContext, redirect

from pnlp_web.utils import get_level_for
from pnlp_web.views import validation
from pnlp_web.decorators import provider_required


@provider_required
def dashboard(request):
    return render(request, 'dashboard.html', {})
