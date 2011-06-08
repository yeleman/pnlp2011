#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from pnlp_core.data import MalariaDataHolder, MalariaReportForm

from pnlp_web.decorators import provider_required
from pnlp_core.models import MalariaReport
from pnlp_core.validators import MalariaReportValidator


@provider_required
def data_browser(request):
    context = {'category': 'raw_data'}
    web_provider = request.user.get_profile()

    report = MalariaReport.validated.all()[0]
    context.update({'report': report})

    form = MalariaReportForm(instance=report)

    context.update({'form': form})

    return render(request, 'raw_data.html', context)
