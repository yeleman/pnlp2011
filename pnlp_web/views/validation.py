#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import datetime

from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, RequestContext, get_object_or_404

from pnlp_core.utils import (provider_entity, current_reporting_period, \
                             get_reports_to_validate, \
                             get_validated_reports, \
                             get_not_received_reports, \
                             time_can_validate, current_period, \
                             contact_for, \
                             time_cscom_over, time_district_over, time_region_over)

from pnlp_web.decorators import provider_required
from pnlp_core.models import MalariaReport


class MalariaReportForm(forms.ModelForm):
    class Meta:
        model = MalariaReport
        exclude = ('_status', 'type', 'receipt', 'period', 'entity', 'created_by', 'created_on', 'modified_by')

@provider_required
def validation_list(request):
    context = {'category': 'validation'}
    web_provider = request.user.get_profile()

    entity = provider_entity(web_provider)
    period = current_reporting_period()

    not_sent = [(ent, contact_for(ent)) for ent in get_not_received_reports(entity, period)]

    context.update({'not_validated': get_reports_to_validate(entity, period),
                    'validated': get_validated_reports(entity, period),
                    'not_sent': not_sent})

    context.update({'is_complete': context['validated'].__len__() == entity.get_children().__len__(), 
                    'is_idle': context['not_validated'].__len__() == 0 and context['not_sent'].__len__() > 0})

    context.update({'time_cscom_over': time_cscom_over(), \
                    'time_district_over': time_district_over(), \
                    'time_region_over': time_region_over()})

    context.update({'validation_over': not time_can_validate(entity)})

    context.update({'current_period': current_period(), 'current_reporting_period': period})

    return render(request, 'validation_list.html', context)

@provider_required
def report_validation(request, report_receipt):
    context = {'category': 'validation'}

    report = get_object_or_404(MalariaReport, receipt=report_receipt)
    context.update({'report': report})

    if request.method == 'POST':
        form = MalariaReportForm(request.POST, instance=report)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = MalariaReportForm(instance=report)

    context.update({'form': form})

    return render(request, 'report_validation.html', context)
