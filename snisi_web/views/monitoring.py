#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou


from django.contrib import messages
from django.shortcuts import render, redirect

from bolibana.web.decorators import provider_permission
from bolibana.models.Entity import Entity

from snisi_core.data import current_period, current_reporting_period
from snisi_core.models.MalariaReport import MalariaR

from malaria.dashboard import nb_reports_for


def sms_for_period(period):
        from nosmsd.models import Inbox, SentItems

        inbox = Inbox.objects.filter(receivingdatetime__gte=period.start_on,
                                     receivingdatetime__lte=period.end_on)\
                             .all().order_by('-receivingdatetime')

        sent = SentItems.objects.filter(sendingdatetime__gte=period.start_on,
                                        sendingdatetime__lte=period.end_on)\
                                .all().order_by('-sendingdatetime')
        list_messages = list(inbox) + list(sent)

        return sorted(list_messages, key=lambda msg: msg.date, reverse=True)


@provider_permission('can_monitor_transmission')
def source_data(request):
    """ stats of transmission """
    context = {'category': 'monitoring', 'location': 'source_data'}

    period = current_reporting_period()

    def entity_dict(entity):
        entity_dict = nb_reports_for(entity, period)
        entity_dict.update({'children': []})
        return entity_dict

    entities = []
    for entity in Entity.objects.filter(type__slug='district'):

        if MalariaR.objects.filter(period=period, entity=entity).count():
            continue

        edata = entity_dict(entity)
        edata['children'] = [entity_dict(e)
                             for e in entity.get_children()
                             if not MalariaR.objects.filter(period=period, entity=e).count()]

        entities.append(edata)

    context.update({'entities': entities})

    return render(request, 'monitoring/monitoring_transmission.html', context)


@provider_permission('can_monitor_transmission')
def messages_log(request):
    """ Display all messages """

    context = {'category': 'monitoring', 'location': 'messages_log'}

    def name_phone(sms):
        """ Search name provider """
        from bolibana.models.Provider import Provider

        if len(sms.identity.split('+223')) == 2:
            indicatif, phone = sms.identity.split('+223')
        else:
            phone = sms.identity.split('+223')[0]

        provider = Provider.objects.filter(phone_number__contains=phone)
        return provider

    all_sms = sms_for_period(current_period())
    for sms in all_sms:
        if name_phone(sms):
            sms.provider = name_phone(sms)[0]

    context.update({'all_sms': all_sms})
    return render(request, 'monitoring/log_message.html', context)


def nb_reports_unvalidated_for(entity, period):
    """ report unvalidated """
    nb_val = MalariaR.validated.filter(entity__parent=entity, period=period).count()
    if entity.type.slug == 'district':
        nb_ent = len([e for e in entity.get_children()
                      if MalariaR.objects.filter(period=period, entity=e).count()])
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
def validation(request):
    """ stats of validation """

    context = {'category': 'monitoring', 'location': 'validation'}

    def entity_dict(entity):
        entity_dict = nb_reports_unvalidated_for(entity, period)
        entity_dict.update({'children': []})
        return entity_dict

    period = current_reporting_period()

    entities = []
    for entity in Entity.objects.filter(type__slug='district'):
        edata = entity_dict(entity)
        edata['children'] = [e for e in entity.get_children()
                             if MalariaR.unvalidated
                                        .filter(period=period, entity=e).count()]
        entities.append(edata)

    context.update({'entities': entities})
    return render(request, 'monitoring/report_unvalidated.html', context)


@provider_permission('can_monitor_transmission')
def bulk_messaging(request):
    from django import forms
    from bolibana.models import Provider
    from nosmsd.utils import send_sms

    context = {'category': 'monitoring', 'location': 'messaging'}

    class MessageForm(forms.Form):
        number = forms.CharField(label=(u"Numéro"))
        text = forms.CharField(widget=forms.Textarea(), label=(u"Texte"))

        def clean_text(self):
            return self.cleaned_data.get('text')[:150]

    form = MessageForm()

    providers = Provider.objects.filter(phone_number__isnull=False)
    all_providers = []
    for pr in providers:
        all_providers.append(("%s %s %s" % (pr.name(), pr.access(),
                                            pr.phone_number), pr.phone_number))
        if pr.phone_number_extra:
            all_providers.append(("%s %s %s" % (pr.name(), pr.access(),
                                  pr.phone_number_extra), pr.phone_number_extra))

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            send_sms(form.cleaned_data.get('number'),
                     form.cleaned_data.get('text'))
            messages.success(request, (u"SMS envoié"))
            return redirect("log_message")

    context.update({'form': form, 'all_providers': all_providers})
    return render(request, 'monitoring/send_message.html', context)
