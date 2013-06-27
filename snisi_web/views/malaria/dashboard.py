#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django import forms
from django.shortcuts import render
# from django.utils.translation import ugettext as _, ugettext_lazy

from nosmsd.models import Inbox, SentItems
from bolibana.web.decorators import provider_required
from snisi_core.models.MalariaReport import MalariaR
from snisi_core.data import current_reporting_period, contact_for


def nb_reports_for(entity, period):
    nb_rec = MalariaR.objects.filter(entity__parent=entity,
                                     period=period).count()
    next_period = period.next()
    if entity.type.slug == 'district':
        nb_ent = entity.get_children().count()
        incoming_sms = None
        all_sms = None
    else:
        nb_ent = 1
        number = contact_for(entity, True).phone_number
        if not number.startswith('+223'):
            number = '+223' + number
        incoming_sms = Inbox.objects.filter(receivingdatetime__gte=next_period.start_on,
                                            receivingdatetime__lte=next_period.end_on,
                                            sendernumber=number)
        sent_sms = SentItems.objects.filter(sendingdatetime__gte=next_period.start_on,
                                            sendingdatetime__lte=next_period.end_on,
                                            destinationnumber=number)
        if incoming_sms.count() != sent_sms.count():
            all_sms = list(incoming_sms) + list(sent_sms)
        else:
            all_sms = sent_sms

    percent = float(nb_rec) / nb_ent
    return {'entity': entity, 'nb_received': nb_rec,
            'nb_expected': nb_ent,
            'received_rate': percent,
            'incoming_sms': incoming_sms,
            'all_sms': all_sms}


@provider_required
def dashboard(request):
    context = {'category': 'malaria', 'location': 'dashboard'}

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
                    'total_cscom': Entity.objects.filter(type__slug='cscom').count(),
                    'time_cscom_over': time_cscom_over(period),
                    'time_district_over': time_district_over(period),
                    'time_region_over': time_region_over(period)})

    received_cscom_reports = received_reports(period, 'cscom')
    cscom_reports_validated = reports_validated(period, 'cscom')
    district_reports_validated = reports_validated(period, 'district')
    reporting_rate = \
        float(MalariaR.validated.filter(period=period).count()) \
        / Entity.objects.count()

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
                                      modified_by__username='autobot')
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


class DateForm(forms.Form):
    import datetime
    date = forms.DateField(initial=datetime.date.today)


def change_date(request):

    context = {}

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            import subprocess
            subprocess.call(['sudo', 'date', form.cleaned_data.get('date').strftime('%m%d1200%Y')])
            context.update({'success': True})
        else:
            pass
    else:
        form = DateForm()

    context.update({'form': form})

    return render(request, 'date.html', context)
