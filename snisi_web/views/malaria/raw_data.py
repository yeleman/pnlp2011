#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _
from django.http import HttpResponse

from bolibana.models.Entity import Entity
from bolibana.models.Period import MonthPeriod
from snisi_core.data import (raw_data_periods_for,
                             entities_path,
                             provider_can_or_403,
                             provider_can,
                             current_reporting_period)
from snisi_core.data.malaria import (MalariaRForm, AggMalariaRForm)

from bolibana.web.decorators import provider_required, provider_permission
from snisi_core.models.MalariaReport import MalariaR, AggMalariaR
from snisi_core.models.GenericReport import GenericReport
from snisi_core.exports import report_as_excel


@provider_permission('can_view_raw_data')
def data_browser(request, entity_code=None, period_str=None):
    context = {'category': 'malaria', 'location': 'raw_data'}
    web_provider = request.user

    root = web_provider.target()

    period = None
    entity = None

    # find period from string or default to current reporting
    if period_str:
        try:
            period = MonthPeriod.find_create_from(year=int(period_str[-4:]),
                                                  month=int(period_str[:2]),
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
        entity = web_provider.target()
    context.update({'entity': entity})

    # check permissions on this entity and raise 403
    provider_can_or_403('can_view_raw_data', web_provider, entity)

    # build entities browser
    context.update({'root': root,
                    'paths': entities_path(root, entity)})

    # build periods list
    all_periods = raw_data_periods_for(entity)
    if period_str and not period in all_periods:
        raise Http404(_(u"No report for that period"))

    # fetch only validated reports
    # unless we're with someone who's in charge of validatiing this.
    is_validator = provider_can('can_validate_aggregated_report',
                                web_provider, entity) \
        or provider_can('can_validate_source_report', web_provider, entity)
    if root == entity and is_validator:
        only_validated = False
    else:
        only_validated = True
    greport = GenericReport(entity=entity, period=period,
                            src_cls=MalariaR, agg_cls=AggMalariaR,
                            only_validated=only_validated)

    # if we're in the case of no validated report
    # but one unvalidated, we'll add the period to the template
    if not period in all_periods and greport.is_present:
        all_periods.insert(0, period)

    # send period variables to template
    context.update({'periods': [(p.middle().strftime('%m%Y'), p.middle())
                                for p in all_periods],
                    'period': period})

    if greport.report:
        context.update({'report': greport.report, 'greport': greport})
        form_cls = AggMalariaRForm if greport.is_aggregated else MalariaRForm
        form = form_cls(instance=greport.report)
        context.update({'form': form})
    else:
        context.update({'no_report': True})

    return render(request, 'malaria/raw_data.html', context)


@provider_required
def excel_export(request, report_receipt):
    context = {'category': 'malaria'}
    web_provider = request.user

    try:
        report = get_object_or_404(MalariaR, receipt=report_receipt)
    except:
        report = get_object_or_404(AggMalariaR, receipt=report_receipt)
    context.update({'report': report})

    # check permission or raise 403
    provider_can_or_403('can_view_raw_data', web_provider, report.entity)

    file_name = 'PNLP_%(entity)s.%(month)s.%(year)s.xls' \
                % {'entity': report.entity.slug,
                   'month': report.period.middle().month,
                   'year': report.period.middle().year}

    file_content = report_as_excel(report).getvalue()

    response = HttpResponse(file_content,
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    response['Content-Length'] = len(file_content)

    return response
