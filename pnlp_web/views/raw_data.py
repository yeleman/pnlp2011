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

    root = web_provider.first_target()

    period = None
    entity = None

    # find period from string or default to current reporting
    if period_str:
        try:
            period = MonthPeriod.find_create_from(year=int(period_str[-4:]), \
                                                  month=int(period_str[:2]), \
                                                  dont_create=True)
        except:
            pass
    if not period:
        period = current_reporting_period()

    # find entity or default to provider target
    # raise 404 on wrong provided entity code
    if entity_code:
        entity = get_object_or_404(Entity, slug=entity_code)

    if not entity:
        entity = web_provider.first_target()
    context.update({'entity': entity})

    # check permissions on this entity and raise 403

    # build entities browser
    context.update({'root': root, \
                    'paths': entities_path(root, entity)})

    # build periods list
    all_periods = raw_data_periods_for(entity)
    if period_str and not period in all_periods:
        raise Http404(_(u"No report for that period"))
    context.update({'periods': [(p.middle().strftime('%m%Y'), p.middle()) \
                                for p in all_periods], \
                    'period': period})

    try:
        report = MalariaReport.validated.get(entity=entity, period=period)
    except MalariaReport.DoesNotExist:
        context.update({'no_report': True})
    else:
        context.update({'report': report})
        form = MalariaReportForm(instance=report)
        context.update({'form': form})

    return render(request, 'raw_data.html', context)
