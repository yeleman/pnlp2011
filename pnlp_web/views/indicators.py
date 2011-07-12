#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.http import Http404
from django.utils.translation import ugettext as _
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


def import_path(name):
        """ import a callable from full module.callable name """
        modname, _, attr = name.rpartition('.')
        if not modname:
            # single module name
            return __import__(attr)
        m = __import__(modname, fromlist=[attr])
        return getattr(m, attr)


@provider_permission('can_view_raw_data')
def indicator_browser(request, entity_code=None, period_str=None, \
                    section_index=1, sub_section=None):
    context = {'category': 'indicator_data'}
    web_provider = request.user.get_profile()

    root = web_provider.first_target()

    periods = []
    speriod = eperiod = None
    entity = None
    section_index = int(section_index) - 1

    # find period from string or default to current reporting
    if period_str:
        speriod_str, eperiod_str = period_str.split('-')
        try:
            speriod = MonthPeriod.find_create_from(\
                                                  year=int(speriod_str[-4:]), \
                                                  month=int(speriod_str[:2]), \
                                                  dont_create=True)
            eperiod = MonthPeriod.find_create_from(\
                                                  year=int(eperiod_str[-4:]), \
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

    # periods variables
    context.update({'periods': [(p.pid, p.middle()) for p in periods], \
                    'period_str': '%s-%s' % (speriod.pid, eperiod.pid), \
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

    from pnlp_core.indicators import INDICATOR_SECTIONS

    context.update({'sections': INDICATOR_SECTIONS})

    try:
        section = INDICATOR_SECTIONS[int(section_index)]
        if not sub_section:
            if len(section['sections']):
                sub_section = section['sections'].keys()[0]
        sname = 'pnlp_core.indicators.section%d' % (section_index + 1)
        if sub_section:
            sname = '%s_%s' % (sname, sub_section.__str__())
        sm = import_path(sname)
    except:
        raise Http404(_(u"This section does not exist."))

    context.update({'section': section, 'sub_section': sub_section})

    context.update({'widgets': [widget(entity=entity, periods=periods) \
                                for widget in sm.WIDGETS]})

    return render(request, 'indicator_data.html', context)
