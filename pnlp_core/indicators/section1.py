#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.utils.translation import ugettext as _

from bolibana_reporting.models import Entity
from bolibana_reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label, blank)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for


class Under5MalariaTable(IndicatorTable):

    name = _(u"Tableau 5")
    title = _(u"Enfants moins de 5 ans")
    caption = _(u"Nombre de cas de paludisme chez les enfants " \
                "de moins de 5 ans")

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Total des cas suspects")
    def total_suspected_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_suspected_malaria_cases

    @blank
    @indicator(1)
    def none(self):
        pass

    @indicator(2, 'total_suspected_cases')
    @label(u". Cas simples")
    def simple_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_simple_malaria_cases

    @label(u". Cas graves")
    @indicator(3, 'total_suspected_cases')
    def severe_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_severe_malaria_cases


class MalariaWithinAllConsultationGraph(IndicatorTable):

    name = _(u"Figure 1")
    title = _(u" ")
    caption = _(u"Proportion des cas de paludisme par rapport aux " \
                "consultations toutes causes confondues")
    type = 'graph'

    default_options = {'with_percentage': True, \
                       'with_reference': False, \
                       'with_data': False, \
                       'only_percent': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    def total_consultations(self, period):
        report = get_report_for(self.entity, period)
        return report.total_consultation_all_causes

    @indicator(1, 'total_consultations')
    @label(u"% consultations pour Paludisme (Tous cas suspectés)")
    def malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_suspected_malaria_cases

WIDGETS = [Under5MalariaTable, MalariaWithinAllConsultationGraph]
