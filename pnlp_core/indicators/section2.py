#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.models import Entity
from bolibana.reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label, blank)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for, find_report_attr_age


class NbreCasSuspectesTestesConfirmes(IndicatorTable):
    """ Graphe: Nombre de cas de paludisme (cas suspects, cas testés, cas

        confirmés) """

    name = u"Figure 2"
    title = u""
    caption = u"Nombre de cas de paludisme (cas suspects, " \
              u"cas testés, cas confirmés) ???."
    type = 'graph'

    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': False}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Cas suspects")
    def total_suspected_malaria_cases(self, period):
        return find_report_attr_age(self.entity, period, \
                               'total_suspected_malaria_cases', \
                               self.options.age)

    @indicator(1, "total_suspected_malaria_cases")
    @label(u"Cas testés")
    def total_tested_malaria_cases(self, period):
        return find_report_attr_age(self.entity, period, \
                               'total_tested_malaria_cases', \
                               self.options.age)

    @indicator(2, "total_suspected_malaria_cases")
    @label(u"Cas confirmés")
    def total_confirmed_malaria_cases(self, period):
        return find_report_attr_age(self.entity, period, \
                               'total_confirmed_malaria_cases', \
                               self.options.age)


class CasSimplesGraves(IndicatorTable):
    """   """

    name = u" "
    title = u" "
    caption = u" "
    type = 'graph'

    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': False}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @indicator(0)
    @label(u"Cas confirmés")
    def total_confirmed_malaria_cases(self, period):
        return find_report_attr_age(self.entity, period, \
                               'total_confirmed_malaria_cases', \
                               self.options.age)

    @indicator(1, "total_confirmed_malaria_cases")
    @label(u"Cas simples")
    def total_simple_malaria_cases(self, period):
        return find_report_attr_age(self.entity, period, \
                               'total_simple_malaria_cases', \
                               self.options.age)

    @indicator(2, "total_confirmed_malaria_cases")
    @label(u"Cas graves")
    def total_severe_malaria_cases(self, period):
        return find_report_attr_age(self.entity, period, \
                               'total_severe_malaria_cases', \
                               self.options.age)


class CasTestes(IndicatorTable):
    """ Graphe: Nombre de cas de paludisme (cas suspects, cas testés, cas

        confirmés) """

    name = u" "
    caption = u" "
    graph_type = 'line'
    type = "graph"
    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Cas suspects")
    def total_suspected_malaria_cases(self, period):
        return find_report_attr_age(self.entity, period, \
                               'total_suspected_malaria_cases', \
                               self.options.age)

    @indicator(1, "total_suspected_malaria_cases")
    @label(u"Cas testés")
    def total_tested_malaria_cases(self, period):
        return find_report_attr_age(self.entity, period, \
                               'total_tested_malaria_cases', \
                               self.options.age)


class CasConfirmes(IndicatorTable):
    """ Graphe: Nombre de cas de paludisme (cas suspects, cas testés, cas

        confirmés) """

    name = u" "
    caption = u" "
    graph_type = 'line'
    type = "graph"
    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Cas suspects")
    def total_suspected_malaria_cases(self, period):
        return find_report_attr_age(self.entity, period, \
                               'total_suspected_malaria_cases', \
                               self.options.age)

    @indicator(1, "total_suspected_malaria_cases")
    @label(u"Cas confirmés")
    def total_confirmed_malaria_cases(self, period):
        return find_report_attr_age(self.entity, period, \
                               'total_confirmed_malaria_cases', \
                               self.options.age)
