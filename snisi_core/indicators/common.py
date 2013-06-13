#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.models.Entity import Entity
from bolibana.reporting.indicators import NoSourceData

from snisi_core.models.MalariaReport import MalariaR, AggMalariaR
from snisi_core.models.GenericReport import GenericReport


class MalariaIndicatorTable(object):

    def period_is_valid(self, period):
        return period_is_valid(entity=self.entity, period=period)


def get_report_for(entity, period, validated=True):
    """ MalariaR for entity and period or raise NoSourceData """
    greport = GenericReport(entity=entity, period=period,
                            src_cls=MalariaR, agg_cls=AggMalariaR,
                            only_validated=validated)
    if greport.is_present:
        return greport.report
    else:
        raise NoSourceData


def get_report_for_element(report, element):
    return report[element]


def period_is_valid(entity, period):
    try:
        return bool(get_report_for(entity, period, True))
    except NoSourceData:
        return False


def period_is_expected(entity, period, validated=True):
    greport = GenericReport(entity=entity, period=period,
                            src_cls=MalariaR, agg_cls=AggMalariaR,
                            only_validated=validated)
    return greport.is_expected


def get_report_national(period, validated=True):
    """ MalariaR for slug entity and period or raise NoSourceData """

    try:
        entity = Entity.objects.get(slug='mali')
    except Entity.DoesNotExist:
        raise NoSourceData

    return get_report_for(entity, period, validated)


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
    for report in MalariaR.objects.filter(type=MalariaR.TYPE_SOURCE,
                                          period=period):
        if (getattr(report, 'stockout_%s' % product) == report.NO
           and (entity in report.entity.get_ancestors()
           or entity == report.entity)):
            nb_stockout += 1
    return nb_stockout
