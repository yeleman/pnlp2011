#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext

from bolibana_reporting.excel import IncorrectReportData, MissingData
from pnlp_core.excel import MalariaExcelForm


def handle_uploaded_file(f):
    """ stores temporary file as a real file for form upload """
    fname = '/tmp/form_%s.xls' % datetime.now().strftime('%s')
    destination = open(fname, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return fname


@login_required
def upload_form(request):
    context = {'category': 'upload'}
    provider = request.user.get_profile()

    if request.method == 'POST':
        if 'excel_form' in request.FILES:
            filepath = handle_uploaded_file(request.FILES['excel_form'])

            status = None
            instance = None

            form = MalariaExcelForm(filepath)
            if form.is_valid():
                try:
                    instance = form.create_report(author=provider)
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

    return render_to_response('upload_form.html', \
                              context, RequestContext(request))
