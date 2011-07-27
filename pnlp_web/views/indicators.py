#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render, redirect, get_object_or_404

from pnlp_core.data import (MalariaDataHolder, \
                            MalariaReportForm, \
                            most_accurate_report, \
                            raw_data_periods_for, \
                            provider_entity, \
                            entities_path, \
                            provider_can_or_403, \
                            current_reporting_period)
from pnlp_web.decorators import provider_required, provider_permission
from bolibana_reporting.models import Entity, MonthPeriod


@provider_permission('can_view_raw_data')
def test_indicators(request, entity_code=None, period_str=None):
    context = {'category': 'indicator_data'}
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
    provider_can_or_403('can_view_indicator_data', web_provider, entity)

    # build entities browser
    context.update({'root': root, \
                    'paths': entities_path(root, entity)})

    return render(request, 'indicator_data.html', context)

