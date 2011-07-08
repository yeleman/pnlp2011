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
def test_indicators(request, entity_code=None, period_str=None, \
                    section=None, sub_section=None):
    context = {'category': 'indicator_data'}
    web_provider = request.user.get_profile()

    root = web_provider.first_target()

    periods = []
    speriod = eperiod = None
    entity = None
    #section = None

    # find period from string or default to current reporting
    if period_str:
        speriod_str, eperiod_str = period_str.split('-')
        try:
            speriod = MonthPeriod.find_create_from(year=int(speriod_str[-4:]), \
                                                  month=int(speriod_str[:2]), \
                                                  dont_create=True)
            eperiod = MonthPeriod.find_create_from(year=int(eperiod_str[-4:]), \
                                                  month=int(eperiod_str[:2]), \
                                                  dont_create=True)
            if speriod.middle() >= eperiod.middle():
                periods = [speriod]
            else:
                period = speriod
                while period.middle() <= eperiod.middle():
                    periods.append(period)
                    period = period.next()
        except:
            pass

    if not speriod or not eperiod:
        speriod = eperiod = current_reporting_period()

    if not periods:
        periods = [speriod]

    print("entity_code: %s" % entity_code)
    print("periods: %s" % periods)
    print("speriod: %s" % speriod)
    print("eperiod: %s" % eperiod)

    # periods variables
    context.update({'periods': [(p.pid, p.middle()) for p in periods], \
                    'speriod': speriod, 'eperiod': eperiod, 'period': speriod})

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

    from pnlp_core.indicators.section1 import *
    table = Under5MalariaTable(entity=entity, periods=periods)
    print(table.data())
    print(table.options)

    graph = MalariaWithinAllConsultationGraph(entity=entity, periods=periods)
    print(graph.data())
    print(graph.options)

    from pnlp_core.indicators import INDICATOR_SECTIONS

    context.update({'sections': sorted(INDICATOR_SECTIONS.items())})

    if section:
        section = INDICATOR_SECTIONS[section]

    context.update({'section': section, 'sub_section': sub_section})

    context.update({'table': table, 'graph': graph})

    return render(request, 'indicator_data.html', context)

