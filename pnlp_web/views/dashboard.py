#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, RequestContext, redirect
from django.utils.translation import ugettext as _, ugettext_lazy
from django.conf import settings

from pnlp_web.decorators import provider_required
from pnlp_core.utils import send_email


def contact_choices(contacts):
    """ returns (a[0], a[1] for a in a list """
    # SUPPORT_CONTACTS contains slug, name, email
    # we need only slug, name for contact form.
    return [(slug, name) for slug, name, email in settings.SUPPORT_CONTACTS]


class ContactForm(forms.Form):
    """ Simple contact form with recipient choice """

    name = forms.CharField(max_length=50, required=True, \
                                 label=ugettext_lazy(u"Your Name"))
    email = forms.EmailField(required=False, \
                             label=ugettext_lazy(u"Your e-mail address"))
    phone_number = forms.CharField(max_length=12, required=False, \
                                   label=ugettext_lazy(u"Your phone number"))
    subject = forms.CharField(max_length=50, required=False, \
                                label=ugettext_lazy(u"Subject"))

    recipient = forms.ChoiceField(required=False, \
                                  label=ugettext_lazy(u"Destinataire"), \
                          choices=contact_choices(settings.SUPPORT_CONTACTS), \
                                  help_text=_(u"Choose PNLP for operational " \
                                              u"requests and ANTIM for " \
                                              u"technical ones."))

    message = forms.CharField(required=True, \
                              label=ugettext_lazy(u"Your request"), \
                              widget=forms.Textarea)


def contact(request):
    category = 'contact'
    context = {}

    try:
        web_provider = request.user.get_profile()
    except:
        web_provider = None

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            try:
                dest_mail = [email for s, n, email \
                                   in settings.SUPPORT_CONTACTS \
                                   if s == 'pnlp'][0]
            except:
                dest_mail = []

            mail_cont = {'provider': web_provider, \
                         'name': form.cleaned_data.get('name'),
                         'email': form.cleaned_data.get('email'),
                         'phone_number': form.cleaned_data.get('phone_number'),
                         'subject': form.cleaned_data.get('subject'),
                         'message': form.cleaned_data.get('message')}

            sent, sent_message = send_email(recipients=dest_mail, \
                                        context=mail_cont,
                                       template='emails/support_request.txt', \
                             title_template='emails/title.support_request.txt')
            if sent:
                messages.success(request, _(u"Support request sent."))
                return redirect('support')
            else:
                messages.error(request, _(u"Unable to send request. Please " \
                                          "try again later."))

    if request.method == 'GET':
        if web_provider:
            initial_data = {'name': web_provider.name_access, \
                          'email': web_provider.email, \
                          'phone_number': web_provider.phone_number}
        else:
            initial_data = {}

        form = ContactForm(initial=initial_data)

    context.update({'form': form})

    return render(request, 'contact.html', context)


@provider_required
def dashboard(request):
    category = 'dashboard'
    context = {}

    from bolibana_reporting.models import Entity
    from pnlp_core.models import MalariaReport
    from pnlp_core.data import (current_period, \
                                current_reporting_period, current_stage, \
                                time_cscom_over, time_district_over, \
                                time_region_over)

    def sms_received_sent_by_period(period):
        from nosms.models import Message
        messages = Message.objects.filter(date__gte=period.start_on, \
                                          date__lte=period.end_on)
        received = Message.objects\
                          .filter(direction=Message.DIRECTION_INCOMING).count()
        sent = messages.filter(direction=Message.DIRECTION_OUTGOING).count()
        return (received, sent)

    current_period = current_period()
    period = current_reporting_period()

    context.update({'current_period': current_period,
                    'current_reporting_period': period,
                    'current_stage': current_stage(),
                    'current_sms': sms_received_sent_by_period(current_period),
                    'current_reporting_sms': \
                         sms_received_sent_by_period(period),
                    'total_cscom': Entity.objects\
                                         .filter(type__slug='cscom').count(),
                    'time_cscom_over': time_cscom_over(period),
                    'time_district_over': time_district_over(period),
                    'time_region_over': time_region_over(period)})

    received_cscom_reports = MalariaReport.objects.filter(period=period, entity__type__slug='cscom').count()
    cscom_reports_validated = MalariaReport.validated.filter(period=period, entity__type__slug='cscom').count()
    district_reports_validated = MalariaReport.validated.filter(period=period, entity__type__slug='district').count()
    reporting_rate = float(MalariaReport.validated.filter(period=period).count()) / Entity.objects.count()

    context.update({'received_cscom_reports': received_cscom_reports,
                    'cscom_reports_validated': cscom_reports_validated,
                    'district_reports_validated': district_reports_validated,
                    'reporting_rate': reporting_rate})

    return render(request, 'dashboard.html', context)
