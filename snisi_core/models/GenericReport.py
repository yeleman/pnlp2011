#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.db.models import Q
from bolibana.models.ExpectedReporting import (ExpectedReporting,
                                               SOURCE_LEVEL,
                                               AGGREGATED_LEVEL)


class GenericReport(object):

    def __init__(self, entity, period,
                 src_cls=None, agg_cls=None, level=None,
                 only_validated=True):

        # storing passed arguments
        self._src_cls = src_cls
        self._agg_cls = agg_cls
        self._level = level
        self._period = period
        self._entity = entity
        self._only_validated = only_validated

        self._is_expected = False
        self._src_expected = False
        self._agg_expected = False

        self._src_report = None
        self._agg_report = None
        self._reports = []

        self._check_expected()

        self._check_present()

    def _check_expected(self):

        all_exp = ExpectedReporting.objects.filter(entity=self.entity,
                                                   period=self.period)
        all_exp = all_exp.filter(Q(report_class__cls=getattr(self._src_cls, '__name__', '')) |
                                 Q(report_class__cls=getattr(self._agg_cls, '__name__', '')))

        if all_exp:
            self._is_expected = True

        for expected in all_exp:
            if expected.level == SOURCE_LEVEL:
                self._src_expected = True
            if expected.level == AGGREGATED_LEVEL:
                self._agg_expected = True

    def _check_present(self):
        if self._src_expected:
            objects = self._src_cls.validated if self._only_validated else self._src_cls.unvalidated
            try:
                self._src_report = objects.get(entity=self.entity,
                                               period=self.period)
            except self._src_cls.DoesNotExist:
                pass

        if self._agg_expected:
            objects = self._agg_cls.validated if self._only_validated else self._agg_cls.unvalidated
            try:
                self._agg_report = objects.get(entity=self.entity,
                                               period=self.period)
            except self._agg_cls.DoesNotExist:
                pass

        if self._src_report or self._agg_report:
            self._is_present = True

        if self._src_report:
            self._reports.append(self._src_report)

        if self._agg_report:
            self._reports.append(self._agg_report)

    @property
    def is_expected(self):
        return self._is_expected

    @property
    def src_expected(self):
        return self._src_expected

    @property
    def agg_expected(self):
        return self._agg_expected

    @property
    def is_present(self):
        return self.src_present or self.agg_present

    @property
    def src_present(self):
        return self._src_report is not None

    @property
    def agg_present(self):
        return self._agg_report is not None

    @property
    def is_source(self):
        try:
            return self.report.REPORTING_LEVEL == SOURCE_LEVEL
        except AttributeError:
            return False

    @property
    def is_aggregated(self):
        return not self.is_source

    @property
    def report(self):
        if self.level:
            if self._level == SOURCE_LEVEL:
                return self.src_report
            elif self._level == AGGREGATED_LEVEL:
                return self.agg_report
            else:
                return None
        else:
            if len(self._reports) == 0:
                return None
            elif len(self._reports) > 1:
                return self._reports
            else:
                return self._reports[-1]

    @property
    def level(self):
        return self._level

    @property
    def expected_levels(self):
        lvls = []
        if self.src_expected:
            lvls.append(SOURCE_LEVEL)
        if self.agg_expected:
            lvls.append(AGGREGATED_LEVEL)
        return lvls

    @property
    def present_levels(self):
        return [r.REPORTING_LEVEL for r in self._reports]

    @property
    def src_report(self):
        return self._src_report

    @property
    def agg_report(self):
        return self._agg_report

    @property
    def src_cls(self):
        return self._src_cls

    @property
    def agg_cls(self):
        return self._agg_cls

    @property
    def period(self):
        return self._period

    @property
    def entity(self):
        return self._entity
