#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import datetime

from django.shortcuts import render

from bolibana.reporting.excel import IncorrectReportData
from snisi_core.excel import MalariaExcelForm
from bolibana.web.decorators import provider_permission


def handle_uploaded_file(f):
    """ stores temporary file as a real file for form upload """
    fname = '/tmp/form_%s.xls' % datetime.now().strftime('%s')
    destination = open(fname, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return fname


@provider_permission('can_submit_report_via_excel')
def upload_form(request):
    context = {'category': 'upload'}
    web_provider = request.user.get_profile()

    if request.method == 'POST':
        if 'excel_form' in request.FILES:
            filepath = handle_uploaded_file(request.FILES['excel_form'])

            status = None
            instance = None

            form = MalariaExcelForm(filepath)
            if form.is_valid(author=web_provider):
                try:
                    instance = form.create_report(author=web_provider)
                    context.update({'instance': instance})
                    status = 'ok'
                except IncorrectReportData:
                    status = 'error'
            else:
                # not valid
                pass

            if form.errors.count() > 0:
                status = 'error'

            context.update({'all_errors': form.errors.all(True)})
        else:
            status = 'nofile'

        context.update({'status': status})

    return render(request, 'upload_form.html', context)
