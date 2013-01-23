#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import shutil
import pprint

from snisi_core.excel import MalariaExcelForm
from bolibana.tools.utils import get_autobot
from bolibana.reporting.excel import IncorrectReportData


def submit_excel_file(filepath, author, success='success', error='error'):

    # store basename
    filename = os.path.basename(filepath)

    print('Submitting %s' % filename)

    # create Excel form from path
    form = MalariaExcelForm(filepath)

    # test all logic checks on form
    if form.is_valid(author=author, bulk_import=True):
        try:
            print("form is valid")
            # create the report.
            form.create_report(author=author)
            print("report created")
            # move file to success folder
            shutil.move(filepath, os.path.join(success, filename))
            return True
        except IncorrectReportData:
            print("can't create report")
            pass
    else:
        print("form is not valid")
    # form is not valid or report failed to create. move to failed folder
    shutil.move(filepath, os.path.join(error, filename))
    # get all errors string and write them to an error file
    errors = form.errors.all(True)
    pprint.pprint(errors)
    err_f = open(os.path.join(error, filename + '.error.txt'), 'w')
    err_f.write(pprint.pformat(errors))
    err_f.close()
    return False


def import_all(src_folder):
    author = get_autobot()
    success_dir = 'success'
    error_dir = 'error'
    if not os.path.exists(success_dir):
        os.makedirs(success_dir)
    if not os.path.exists(error_dir):
        os.makedirs(error_dir)
    for fname in os.listdir(src_folder):
        if not fname.endswith('.xls'):
            print('skipping %s' % fname)
            continue
        submit_excel_file(os.path.join(src_folder, fname),
                          author, success_dir, error_dir)


def cleanup_db():
    from snisi_core.models.MalariaReport import MalariaR
    from snisi_core.alert import Alert

    # CIV, VY (all)
    MalariaR.objects.filter(entity__parent__slug='bamako').delete()

    # Bamako (all)
    MalariaR.objects.filter(entity__slug='bamako').delete()

    # Mali (all)
    MalariaR.objects.filter(entity__slug='mali').delete()

    # Alert CSCOM 11, 12, 01
    Alert.objects.filter(alert_id__in=('112011', '122011', '012012')).delete()

    # Alert District 11, 12, 01
    Alert.objects.filter(alert_id__in=('district_112011', 'district_122011', 'district_012012')).delete()

    # Alert District 11, 12, 01
    Alert.objects.filter(alert_id__in=('region_112011', 'region_122011', 'region_012012')).delete()
