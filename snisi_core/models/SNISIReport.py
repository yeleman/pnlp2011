#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from bolibana.models.Report import Report
from bolibana.models.IndividualReport import IndividualReport
from bolibana.models.Period import WeekPeriod, MonthPeriod
from bolibana.tools.utils import generate_receipt
from bolibana.models.ExpectedReporting import AGGREGATED_LEVEL


class CommonSNISIReport(object):

    @property
    def arrived_late(self):
        return getattr(self, 'is_late', False)

    @property
    def arrived_late_on_time(self):
        return not self.arrived_late

    @property
    def is_aggregated(self):
        return False

    @property
    def is_source(self):
        return not self.is_aggregated


class SNISIReport(Report, CommonSNISIReport):

    class Meta:
        app_label = 'snisi_core'
        abstract = True

    def to_dict(self):
        d = {}
        for field in self.data_fields():
            d[field] = getattr(self, field)
        return d

    def get(self, slug):
        return getattr(self, slug)

    def field_name(self, slug):
        return self._meta.get_field(slug).verbose_name

    def validate(self):
        return {}

    def fill_blank(self):
        pass

    @classmethod
    def data_fields(cls):
        return []

    @classmethod
    def generate_receipt(cls, instance):
        return generate_receipt(instance, fix='-UNSET', add_random=True)

    @classmethod
    def start(cls, period, entity, author, type=Report.TYPE_SOURCE,
              is_late=False, *args, **kwargs):
        report = cls(period=period, entity=entity, created_by=author,
                     modified_by=author, _status=cls.STATUS_CREATED,
                     type=type)
        for arg, value in kwargs.items():
            try:
                setattr(report, arg, value)
            except AttributeError:
                pass
        return report

    @property
    def mperiod(self):
        """ casted period to MonthPeriod """
        mp = self.period
        mp.__class__ = MonthPeriod
        return mp

    @property
    def wperiod(self):
        """ casted period to WeekPeriod """
        wp = self.period
        wp.__class__ = WeekPeriod
        return wp

    def casted_period(self, cls):
        cp = self.period
        cp.__class__ = cls
        return cp

    @property
    def is_aggregated(self):
        level = getattr(self, 'REPORTING_LEVEL')
        if level is not None:
            return level == AGGREGATED_LEVEL
        lvl_type = getattr(self, 'type')
        if lvl_type is not None:
            return lvl_type == self.TYPE_AGGREGATED
        return False


class SNISIIndividualReport(IndividualReport, CommonSNISIReport):

    class Meta:
        app_label = 'snisi_core'
        abstract = True

    pass
