#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

from django import forms
from django.shortcuts import render
from bolibana.web.decorators import provider_required
from pnlp_core.data import current_period, contact_for
from pnlp_core.models import MalariaReport
from dashboard import nb_reports_for
from bolibana.models import Entity


def sms_for_period(period):
        from nosms.models import Message
        messages = Message.objects.filter(date__gte=period.start_on, \
                                          date__lte=period.end_on).all().order_by('-date')
        return messages

@provider_required
def transmission(request):
    """ stats of transmission """
    context = {'category': 'transmission'}

    period = current_reporting_period()

    def entity_dict(entity):
        entity_dict = nb_reports_for(entity, period)
        entity_dict.update({'children': []})
        return entity_dict
    
    entities = []
    for entity in Entity.objects.filter(type__slug='district'):

        if MalariaReport.objects.filter(period=period, entity=entity).count():
            continue

        edata = entity_dict(entity)
        edata['children'] = [entity_dict(e) \
                             for e in entity.get_children() \
                             if not MalariaReport.objects.filter(period=period, entity=e).count()]

        entities.append(edata)

    context.update({'entities': entities})

    return render(request, 'transmission.html', context)

@provider_required
def log_message(request):
    """ Display all messages """
    context = {'category': 'log_message'}
    all_sms = sms_for_period(current_period())
    context.update({'all_sms': all_sms})
    return render(request, 'log_message.html', context)

@provider_required
def report_validated(request):
	context = {'category': 'report_validated'}
	return render(request, 'report_validated.html', context)