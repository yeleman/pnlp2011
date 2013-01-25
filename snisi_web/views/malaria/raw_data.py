#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _
from django.http import HttpResponse

from bolibana.models.Entity import Entity
from bolibana.models.Period import MonthPeriod
from snisi_core.data import (MalariaRForm,
                            raw_data_periods_for,
                            entities_path,
                            provider_can_or_403,
                            current_reporting_period)
from bolibana.web.decorators import provider_required, provider_permission
from snisi_core.models.MalariaReport import MalariaR
from snisi_core.exports import report_as_excel


@provider_permission('can_view_raw_data')
def data_browser(request, entity_code=None, period_str=None):
    context = {'category': 'raw_data', 'menu': 'palu'}
    web_provider = request.user.get_profile()

    root = web_provider.first_target()

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
        entity = web_provider.first_target()
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

    try:
        # get validated report for that period and location
        report = MalariaR.validated.get(entity=entity, period=period)
    except MalariaR.DoesNotExist:
        # district users need to be able to see the generated report
        # which have been created based on their validations/data.
        # if a district is looking at its root district and report exist
        # but not validated, we show it (with period) and no valid flag
        if web_provider.first_role().slug == 'district' and root == entity:
            try:
                report = MalariaR.unvalidated.get(entity=entity,
                                                  period=period)
                if not period in all_periods:
                    all_periods.insert(0, period)
            except:
                report = None
        else:
            report = None

    # send period variables to template
    context.update({'periods': [(p.middle().strftime('%m%Y'), p.middle())
                                for p in all_periods],
                    'period': period})

    if report:
        context.update({'report': report})
        form = MalariaRForm(instance=report)
        context.update({'form': form})
    else:
        context.update({'no_report': True})

    return render(request, 'raw_data.html', context)


@provider_required
def excel_export(request, report_receipt):
    context = {'category': 'raw_data', 'menu': 'palu'}
    web_provider = request.user.get_profile()

    report = get_object_or_404(MalariaR, receipt=report_receipt)
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
