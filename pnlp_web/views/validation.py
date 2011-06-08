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
from pnlp_core.validators import MalariaReportValidator


class MalariaReportForm(forms.ModelForm):
    class Meta:
        model = MalariaReport
        exclude = ('_status', 'type', 'receipt', 'period', \
                   'entity', 'created_by', 'created_on', 'modified_by')

class MalariaDataHolder(object):

    def get(self, slug):
        return getattr(self, slug)

    def field_name(self, slug):
        return MalariaReport._meta.get_field(slug).verbose_name

    def set(self, slug, data):
        try:
            setattr(self, slug, data)
        except AttributeError:
            exec 'self.%s = None' % slug
            setattr(self, slug, data)

    def fields_for(self, cat):
        u5fields = ['u5_total_consultation_all_causes', \
                    'u5_total_suspected_malaria_cases', \
                    'u5_total_simple_malaria_cases', \
                    'u5_total_severe_malaria_cases', \
                    'u5_total_tested_malaria_cases', \
                    'u5_total_confirmed_malaria_cases', \
                    'u5_total_treated_malaria_cases', \
                    'u5_total_inpatient_all_causes', \
                    'u5_total_malaria_inpatient', \
                    'u5_total_death_all_causes', \
                    'u5_total_malaria_death', \
                    'u5_total_distributed_bednets']
        if cat == 'u5':
            return u5fields
        if cat == 'o5':
            return [f.replace('u5', 'o5') for f in u5fields][:-1]
        if cat == 'pw':
            fields = [f.replace('u5', 'pw') for f in u5fields]
            fields.remove('pw_total_simple_malaria_cases')
            fields.extend(['pw_total_anc1', 'pw_total_sp1', 'pw_total_sp2'])
            return fields
        if cat == 'so':
            return ['stockout_act_children', \
                    'stockout_act_youth', \
                    'stockout_act_adult', \
                    'stockout_artemether', \
                    'stockout_quinine', \
                    'stockout_serum', \
                    'stockout_bednet', \
                    'stockout_rdt', \
                    'stockout_sp']

    def data_for_cat(self, cat, as_dict=False):
        data = []
        for field in self.fields_for(cat):
            data.append(self.get(field))
        return data

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
            #print(form.cleaned_data)
            print("DJANGO VALID")
            data_browser = MalariaDataHolder()

            # feed data holder with sms provided data
            for key in form.cleaned_data:
                if key.split('_')[0] in ('u5', 'o5', 'pw', 'stockout'):
                    data_browser.set(key, form.cleaned_data.get(key))

            # feed data holder with guessable data
            data_browser.set('month', report.period.middle().month)
            data_browser.set('year', report.period.middle().year)
            data_browser.set('hc', report.entity.slug)
            data_browser.set('fillin_day', report.created_on.day)
            data_browser.set('fillin_month', report.created_on.month)
            data_browser.set('fillin_year', report.created_on.year)
            data_browser.set('author', report.created_by.name())

            # create validator and fire
            validator = MalariaReportValidator(data_browser, data_only=True)
            try:
                validator.validate()
            except AttributeError as e:
                message.respond(error_start + e.__str__())
                return True
            errors = validator.errors
            print(data_browser)
            print(data_browser.u5_total_simple_malaria_cases)
            if errors.count() > 0:
                print("VALIDATION ERROR")
                print(errors.all(True))
            else:
                print("NO ERRORS! YAY")
        else:
            print("DJANGO NOT VALID")
            print(form.errors)
    else:
        form = MalariaReportForm(instance=report)

    context.update({'form': form})

    return render(request, 'report_validation.html', context)
