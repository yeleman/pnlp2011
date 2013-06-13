#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import render

from nosmsd.models import Inbox, SentItems
from bolibana.web.decorators import provider_required
from snisi_core.models.MalariaReport import MalariaR
from snisi_core.data import current_reporting_period, contact_for


@provider_required
def dashboard(request):
    category = 'dashboard'
    context = {'category': category, 'menu': 'reprod'}

    from bolibana.models.Entity import Entity
    from snisi_core.data import (current_period, current_stage,
                                 time_cscom_over, time_district_over,
                                 time_region_over)

    def sms_received_sent_by_period(period):
        received = Inbox.objects.filter(receivingdatetime__gte=period.start_on,
                                        receivingdatetime__lte=period.end_on) \
                                .count()
        sent = SentItems.objects.filter(sendingdatetime__gte=period.start_on,
                                        sendingdatetime__lte=period.end_on) \
                                .count()
        return (received, sent)

    def received_reports(period, type_):
        return MalariaR.objects.filter(period=period,
                                       entity__type__slug=type_)

    def reports_validated(period, type_):
        return MalariaR.validated.filter(period=period,
                                         entity__type__slug=type_)

    # def reporting_rate(period, entity):
    #     return float(MalariaR.validated.filter(period=period,
    #                                            entity__parent=entity).count()) \
    #         / Entity.objects.filter(parent__slug=entity.slug).count()

    current_period = current_period()
    period = current_reporting_period()

    context.update({'current_period': current_period,
                    'current_reporting_period': period,
                    'current_stage': current_stage(),
                    'current_sms': sms_received_sent_by_period(current_period),
                    'current_reporting_sms': sms_received_sent_by_period(period),
                    'total_cscom': Entity.objects
                                         .filter(type__slug='cscom').count(),
                    'time_cscom_over': time_cscom_over(period),
                    'time_district_over': time_district_over(period),
                    'time_region_over': time_region_over(period)})

    received_cscom_reports = received_reports(period, 'cscom')
    cscom_reports_validated = reports_validated(period, 'cscom')
    district_reports_validated = reports_validated(period, 'district')
    reporting_rate = float(MalariaR.validated.filter(period=period).count()) / Entity.objects.count()

    cscom_missed_report = \
        Entity.objects.filter(type__slug='cscom')\
                      .exclude(id__in=[r.entity.id
                                       for r
                                       in received_cscom_reports])\
                      .order_by('name')

    def entities_autoreports(level):
        districts_missed_report = {}
        auto_validated_cscom_reports = \
            MalariaR.validated.filter(entity__type__slug=level,
                                      modified_by__user__username='autobot')
        for report in auto_validated_cscom_reports:
            if not report.entity.parent.slug in districts_missed_report:
                districts_missed_report[report.entity.parent.slug] = \
                    {'entity': report.entity.parent,
                     'nbauto': 0,
                     'contact': contact_for(report.entity.parent, False)}
            districts_missed_report[report.entity.parent.slug]['nbauto'] += 1
        return districts_missed_report

    districts_missed_report = entities_autoreports('cscom')
    regions_missed_report = entities_autoreports('district')

    context.update({'received_cscom_reports': received_cscom_reports.count(),
                    'cscom_reports_validated': cscom_reports_validated.count(),
                    'district_reports_validated': district_reports_validated.count(),
                    'reporting_rate': reporting_rate,
                    'cscom_missed_report_count': cscom_missed_report.count(),
                    'cscom_missed_report': [(e, contact_for(e, True))
                                            for e in cscom_missed_report[:20]],
                    'districts_missed_report': districts_missed_report,
                    'regions_missed_report': regions_missed_report})

    return render(request, 'malaria/dashboard.html', context)
