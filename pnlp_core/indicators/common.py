#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from pnlp_core.models import MalariaReport
from bolibana.reporting.indicators import NoSourceData


def get_report_for(entity, period, validated=True):
    """ MalariaReport for entity and period or raise NoSourceData """
    try:
        if validated:
            return MalariaReport.validated.get(entity=entity, period=period)
        else:
            return MalariaReport.unvalidated.get(entity=entity, period=period)
    except MalariaReport.DoesNotExist:
        raise NoSourceData


def report_attr_age(report, attribute, age_code='all'):
    age_prefix = ''
    if age_code == 'all':
        pass
    elif age_code in ('under_five', 'u5'):
        age_prefix = 'u5'
    elif age_code in ('over_five', 'o5'):
        age_prefix = 'o5'
    elif age_code in ('pregnant_women', 'pw'):
        age_prefix = 'pw'
    if age_prefix:
        attr = '%s_%s' % (age_prefix, attribute)
    else:
        attr = attribute
    return getattr(report, attr)


def find_report_attr_age(entity, period, attribute, age_code='all'):
    report = get_report_for(entity, period)
    return report_attr_age(report, attribute, age_code)


def nb_stockout(entity, period, product):
    nb_stockout = 0
    for report in MalariaReport.objects.filter(type=MalariaReport.TYPE_SOURCE,
                                               period=period):
        if (getattr(report, 'stockout_%s' % product) == report.NO
            and (entity in report.entity.get_ancestors()
            or entity == report.entity)):
            nb_stockout += 1
    return nb_stockout
