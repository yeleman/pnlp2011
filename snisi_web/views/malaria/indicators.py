#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.http import Http404
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404

from bolibana.web.decorators import provider_permission
from bolibana.models.Entity import Entity
from bolibana.models.Period import MonthPeriod
from snisi_core.models.MalariaReport import MalariaR, AggMalariaR
from snisi_core.models.GenericReport import GenericReport
from snisi_core.data import (entities_path,
                            provider_can_or_403,
                            current_reporting_period, contact_for)


def import_path(name):
        """ import a callable from full module.callable name """
        modname, __, attr = name.rpartition('.')
        if not modname:
            # single module name
            return __import__(attr)
        m = __import__(modname, fromlist=[attr])
        return getattr(m, attr)


@provider_permission('can_view_raw_data')
def indicator_browser(request, entity_code=None, period_str=None,
                    section_index='1', sub_section=None):
    context = {'category': 'malaria', 'location': 'indicator_data'}
    web_provider = request.user.get_profile()

    root = web_provider.first_target()

    periods = []
    speriod = eperiod = None
    entity = None
    #section_index = int(section_index) - 1

    # find entity or default to provider target
    # raise 404 on wrong provided entity code
    if entity_code:
        entity = get_object_or_404(Entity, slug=entity_code)

    if not entity:
        entity = web_provider.first_target()
    context.update({'entity': entity})

    # define a list of all possible periods.
    # this is the list of all existing MonthPeriod anterior to current
    def all_anterior_periods(period):
        return MonthPeriod.objects\
                          .filter(start_on__lte=period.start_on)\
                          .order_by('start_on')

    all_periods = list(all_anterior_periods(current_reporting_period()).all())
    greport = GenericReport(entity=entity, period=current_reporting_period(),
                            src_cls=MalariaR, agg_cls=AggMalariaR,
                            only_validated=True)
    if not greport.is_expected:
        all_periods.remove(current_reporting_period())

    # retrieve Periods from string
    # if period_string include innexistant periods -> 404.
    if period_str:
        speriod_str, eperiod_str = period_str.split('-')
        try:
            speriod = MonthPeriod.find_create_from(\
                                                  year=int(speriod_str[-4:]),
                                                  month=int(speriod_str[:2]),
                                                  dont_create=True)
            eperiod = MonthPeriod.find_create_from(\
                                                  year=int(eperiod_str[-4:]),
                                                  month=int(eperiod_str[:2]),
                                                  dont_create=True)

            # loop on Period.next() from start one to end one.
            period = speriod
            while period.middle() <= eperiod.middle():
                periods.append(period)
                period = period.next()
        except:
            raise Http404(_(u"Requested period interval (%(period_str)s) " \
                            u"includes inexistant periods.") \
                          % {'period': period_str})

    # in case user did not request a specific interval
    # default to current_reporting_period
    if not speriod or not eperiod:
        speriod = eperiod = current_reporting_period()
        periods = [speriod]

    print('yyy')
    print(speriod)
    print(speriod.__class__)
    print(eperiod)
    print(eperiod.__class__)

    # if end period is before start period, redirect to opposite
    if eperiod < speriod:
        print('exi')
        return redirect('malaria_indicator_data',
                        entity_code=entity.slug,
                        period_str='%s-%s' % (eperiod.pid, speriod.pid))
    print('y2')
    # periods variables
    context.update({'period_str': '%s-%s' % (speriod.pid, eperiod.pid),
                    'speriod': speriod, 'eperiod': eperiod})
    context.update({'periods': [(p.pid, p) for p in periods],
                    'all_periods': [(p.pid, p) for p in all_periods]})
    print('y3')

    # check permissions on this entity and raise 403
    provider_can_or_403('can_view_indicator_data', web_provider, entity)

    # build entities browser
    context.update({'root': root,
                    'paths': entities_path(root, entity)})

    from snisi_core.indicators import INDICATOR_SECTIONS
    print('y4')
    context.update({'sections': \
                    sorted(INDICATOR_SECTIONS.values(),
                          cmp=lambda a, b: int(a['id'].strip('a').strip('b')) \
                                        - int(b['id'].strip('a').strip('b')))})

    try:
        section = INDICATOR_SECTIONS[section_index]
        if not sub_section:
            if len(section['sections']):
                sub_section = section['sections'].keys()[0]
        sname = 'snisi_core.indicators.section%s' % section_index.__str__()
        if sub_section:
            sname = '%s_%s' % (sname, sub_section.__str__())
        sm = import_path(sname)
    except:
        raise
        raise Http404(_(u"This section does not exist."))

    # section 1 specifics
    if section_index == '1':
        context.update({'contact': contact_for(entity)})

    context.update({'section': section, 'sub_section': sub_section})

    context.update({'widgets': [widget(entity=entity, periods=periods) \
                                for widget in sm.WIDGETS]})
    from pprint import pprint as pp ; pp(context)

    return render(request, 'malaria/indicator_data.html', context)
