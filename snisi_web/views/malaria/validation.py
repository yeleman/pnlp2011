#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import datetime

import reversion
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from snisi_core.data import (provider_entity, current_reporting_period,
                             get_reports_to_validate,
                             get_validated_reports,
                             get_not_received_reports,
                             time_can_validate, current_period,
                             contact_for,
                             time_cscom_over, time_district_over,
                             time_region_over)
from snisi_core.data.malaria import (MalariaDataHolder,
                                     MalariaRForm,
                                     AggMalariaRForm)

from bolibana.web.decorators import provider_permission
from snisi_core.models.MalariaReport import MalariaR, AggMalariaR
from snisi_core.validators.malaria import MalariaRValidator
from snisi_core.data import provider_can_or_403


@provider_permission('can_validate_report')
def validation_list(request):
    context = {'category': 'malaria', 'location': 'validation'}
    web_provider = request.user.get_profile()

    entity = provider_entity(web_provider)
    period = current_reporting_period()

    # check permission or raise 403
    # should never raise as already checked by decorator
    provider_can_or_403('can_validate_report', web_provider, entity)

    not_sent = [(ent, contact_for(ent)) \
                for ent in get_not_received_reports(entity, period)]

    context.update({'not_validated': get_reports_to_validate(entity, period),
                    'validated': get_validated_reports(entity, period),
                    'not_sent': not_sent})

    context.update({'is_complete': context['validated'].__len__() == \
                                   entity.get_children().__len__(),
                    'is_idle': context['not_validated'].__len__() == 0 \
                               and context['not_sent'].__len__() > 0})

    context.update({'time_cscom_over': time_cscom_over(),
                    'time_district_over': time_district_over(),
                    'time_region_over': time_region_over()})

    context.update({'validation_over': not time_can_validate(entity)})

    context.update({'current_period': current_period(),
                    'current_reporting_period': period})

    return render(request, 'malaria/validation_list.html', context)


@provider_permission('can_validate_report')
def report_validation(request, report_receipt):
    context = {'category': 'malaria', 'location': 'validation'}
    web_provider = request.user.get_profile()
    type_report = 'MalariaR'
    try:
        report = get_object_or_404(MalariaR, receipt=report_receipt)
    except:
        type_report = 'AggMalariaR'
        report = get_object_or_404(AggMalariaR, receipt=report_receipt)

    context.update({'report': report})

    # check permission or raise 403
    provider_can_or_403('can_validate_report', web_provider, report.entity)

    if request.method == 'POST':
        if type_report == 'MalariaR':
            form = MalariaRForm(request.POST, instance=report)
        else:
            form = AggMalariaRForm(request.POST, instance=report)
        if form.is_valid():
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
            validator = MalariaRValidator(data_browser, data_only=True,
                                          is_editing=True,
                                          level=web_provider.first_role().slug)
            validator.errors.reset()
            try:
                validator.validate()
            except Exception as e:
                print(u"Exception on form validation. "
                      u"Report %(id)d with %(e)r" % {'id': report.id, 'e': e})
                raise
            if validator.errors.count() > 0:
                # validation errors
                context.update({'all_errors': validator.errors.all(True)})
            else:
                # no validation error neither
                # save report
                new_report = form.save(commit=False)
                new_report.modified_by = web_provider
                new_report.modified_on = datetime.now()
                with reversion.create_revision():
                    new_report.save()
                    reversion.set_user(web_provider.user)
                    #new_report.save()

                context.update({'saved': True, 'report': new_report})
        else:
            # django form validation errors
            pass
    else:
        if type_report == 'MalariaR':
            form = MalariaRForm(instance=report)
        else:
            form = AggMalariaRForm(instance=report)

    context.update({'form': form})

    return render(request, 'malaria/report_validation.html', context)


@provider_permission('can_validate_report')
def report_do_validation(request, report_receipt):
    context = {'category': 'malaria', 'location': 'validation'}
    web_provider = request.user.get_profile()

    try:
        report = get_object_or_404(MalariaR, receipt=report_receipt)
    except:
        report = get_object_or_404(MalariaR, receipt=report_receipt)

    # check permission or raise 403
    provider_can_or_403('can_validate_report', web_provider, report.entity)

    report._status = MalariaR.STATUS_VALIDATED
    report.modified_by = web_provider
    report.modified_on = datetime.now()
    with reversion.create_revision():
        report.save()
        reversion.set_user(web_provider.user)
    context.update({'report': report})

    messages.info(request, u"Le rapport %(receipt)s de %(entity)s " \
                           u"a été validé." % {'receipt': report.receipt,
                                              'entity': report.entity})
    return redirect('validation')
