#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from pnlp_core.data import (MalariaDataHolder, \
                            MalariaReportForm, \
                            most_accurate_report, \
                            raw_data_periods_for, \
                            provider_entity, \
                            current_reporting_period)

from bolibana_reporting.models import Entity
from pnlp_web.decorators import provider_required
from pnlp_core.models import MalariaReport
from pnlp_core.validators import MalariaReportValidator


@provider_required
def data_browser(request, entity_code=None, period_str=None):
    context = {'category': 'raw_data'}
    web_provider = request.user.get_profile()

    period = None
    entity = None

    if period_str:
        period = None

    if entity_code:
        entity = None

    if not period:
        period = current_reporting_period()

    if not entity:
        entity = Entity.objects.get(slug='dior')

    print(entity)

    root = provider_entity(web_provider)

    report = most_accurate_report(web_provider, period)
    if not report:
        context.update({'no_report': True})
    else:
        context.update({'periods': [(p.id, p.middle()) for p in raw_data_periods_for(report.entity)], \
                        'period': period})
        context.update({'root': root})
        context.update({'report': report})
        form = MalariaReportForm(instance=report)
        context.update({'form': form})

    return render(request, 'raw_data.html', context)
