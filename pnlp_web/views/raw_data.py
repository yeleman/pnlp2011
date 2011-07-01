#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _

from pnlp_core.data import (MalariaDataHolder, \
                            MalariaReportForm, \
                            most_accurate_report, \
                            raw_data_periods_for, \
                            provider_entity, \
                            entities_path, \
                            current_reporting_period)

from bolibana_reporting.models import Entity, MonthPeriod
from pnlp_web.decorators import provider_required
from pnlp_core.models import MalariaReport
from pnlp_core.validators import MalariaReportValidator


@provider_required
def data_browser(request, entity_code=None, period_str=None):
    context = {'category': 'raw_data'}
    web_provider = request.user.get_profile()

    root = provider_entity(web_provider)

    period = None
    entity = None

    if period_str:
        try:
            period = MonthPeriod.find_create_from(year=int(period_str[-4:]), month=int(period_str[:2]), dont_create=True)
        except:
            pass

    if entity_code:
        entity = get_object_or_404(Entity, slug=entity_code)

    if not period:
        period = current_reporting_period()

    report = most_accurate_report(web_provider, period)

    if not report:
        context.update({'no_report': True})

    else:

        if not entity:
            entity = report.entity

        all_periods = raw_data_periods_for(report.entity)
        if period_str and not period in all_periods:
            raise Http404(_(u"No report for that period"))

        context.update({'periods': [(p.id, p.middle()) for p in all_periods], \
                        'period': period})
        context.update({'root': root, 'paths': entities_path(root, entity)})
        context.update({'report': report})
        form = MalariaReportForm(instance=report)
        context.update({'form': form})

    return render(request, 'raw_data.html', context)
