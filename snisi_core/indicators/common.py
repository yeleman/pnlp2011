#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from snisi_core.models import MalariaReport
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


def get_report_for_element(report, element):
    return report[element]


def get_report_for_slug(entity, period, validated=True):
    """ MalariaReport for slug entity and period or raise NoSourceData """
    try:
        if validated:
            return MalariaReport.validated.get(entity__slug=entity.slug,
                                               period=period)
        else:
            return MalariaReport.unvalidated.get(entity__slug=entity.slug,
                                                 period=period)
    except MalariaReport.DoesNotExist:
        raise NoSourceData


def get_report_national(period, validated=True):
    """ MalariaReport for slug entity and period or raise NoSourceData """
    try:
        if validated:
            return MalariaReport.validated.get(entity__slug="mali",
                                               period=period)
        else:
            return MalariaReport.unvalidated.get(entity__slug="mali",
                                                 period=period)
    except MalariaReport.DoesNotExist:
        raise NoSourceData


def report_attr_age(report, attribute, age_code='all'):
    age_prefix = ''
    age_prefix1 = ''
    age_prefix2 = ''
    if age_code == 'all':
        pass
    elif age_code in ('under_five', 'u5'):
        age_prefix = 'u5'
    elif age_code in ('over_five', 'o5'):
        age_prefix = 'o5'
    elif age_code in ('pregnant_women', 'pw'):
        age_prefix = 'pw'
    elif age_code in ('all_over_five'):
        age_prefix1 = 'o5'
        age_prefix2 = 'pw'

    if age_prefix:
        attr = '%s_%s' % (age_prefix, attribute)
    else:
        attr = attribute
    if age_prefix1 and age_prefix2:
        attr1 = '%s_%s' % (age_prefix1, attribute)
        attr2 = '%s_%s' % (age_prefix2, attribute)
        return getattr(report, attr1), getattr(report, attr2)

    return getattr(report, attr)


def find_report_attr_age(entity, period, attribute, age_code='all'):
    report = get_report_for(entity, period)
    if age_code == ('all_over_five'):
        report1, report2 = report_attr_age(report, attribute, age_code)
        rep = report1 + report2
        return rep
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
