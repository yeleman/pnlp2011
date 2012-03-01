#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou


from django.shortcuts import render
from bolibana.web.decorators import provider_permission
from pnlp_core.data import current_period, current_reporting_period
from pnlp_core.models import MalariaReport
from dashboard import nb_reports_for
from bolibana.models import Entity


def sms_for_period(period):
        from nosms.models import Message
        messages = Message.objects.filter(date__gte=period.start_on, \
                                          date__lte=period.end_on).all() \
                                  .order_by('-date')
        return messages


@provider_permission('can_monitor_transmission')
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
                             if not MalariaReport.objects \
                                    .filter(period=period, entity=e).count()]

        entities.append(edata)

    context.update({'entities': entities})

    return render(request, 'transmission.html', context)


@provider_permission('can_monitor_transmission')
def log_message(request):
    """ Display all messages """
    context = {'category': 'log_message'}
    all_sms = sms_for_period(current_period())
    context.update({'all_sms': all_sms})
    return render(request, 'log_message.html', context)


def nb_reports_unvalidated_for(entity, period):
    nb_val = MalariaReport.validated.filter(entity__parent=entity,
                                              period=period).count()
    if entity.type.slug == 'district':
        nb_ent = len([e for e in entity.get_children() \
            if MalariaReport.objects.filter(period=period, entity=e)\
                            .count()])
    else:
        nb_ent = 1

    try:
        percent = float(nb_val) / nb_ent
    except ZeroDivisionError:
        percent = 0

    return {'entity': entity, 'nb_expected': nb_ent,
            'nb_valideted': nb_val,
            'validation_rate': percent}


@provider_permission('can_monitor_transmission')
def report_unvalidated(request):
    """ stats of validation """

    def entity_dict(entity):
        entity_dict = nb_reports_unvalidated_for(entity, period)
        entity_dict.update({'children': []})
        return entity_dict

    context = {'category': 'transmission'}
    period = current_reporting_period()

    entities = []
    for entity in Entity.objects.filter(type__slug='district'):
        edata = entity_dict(entity)
        edata['children'] = [e for e in entity.get_children() \
                               if MalariaReport.unvalidated \
                               .filter(period=period, entity=e).count()]
        entities.append(edata)

    context.update({'entities': entities})
    return render(request, 'report_unvalidated.html', context)
