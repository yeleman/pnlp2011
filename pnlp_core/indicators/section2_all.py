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
from pnlp_core.indicators.section2 import NbreCasSuspectesTestesConfirmes


class TousCasPaludismeNotifies(IndicatorTable):
    """Tableau: Nombre de cas de paludisme (tout âge confondu) notifiés """

    name = u"Tableau 2.1a"
    title = u"Tout âge confondu"
    caption = u"Nombre de cas de paludisme (tout âge confondu) notifiés"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Total consultation toutes causes confondues (TCC)")
    def total_consultation_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.total_consultation_all_causes

    def blank(self):
        pass
    blank._is_blank = True
    blank._index = 1
    blank._is_indicator = True

    @reference
    @indicator(2, 'total_consultation_all_causes')
    @label(u"Nombre de cas de paludisme (tous suspectés)")
    def total_suspected_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_suspected_malaria_cases

    @indicator(3, 'total_suspected_malaria_cases')
    @label(u". Cas simples")
    def total_simple_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_simple_malaria_cases

    @label(u". Cas graves")
    @indicator(4, 'total_suspected_malaria_cases')
    def total_severe_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_severe_malaria_cases

    def blank_again(self):
        pass
    blank_again._is_blank = True
    blank_again._index = 5
    blank_again._is_indicator = True

    @reference
    @indicator(6, 'total_consultation_all_causes')
    @label(u"Total des cas suspects testés (GE et/ou TDR)")
    def total_tested_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_tested_malaria_cases

    @indicator(7, 'total_tested_malaria_cases')
    @label(u"Nombre de cas suspects testés qui sont confirmés par GE ou TDR")
    def total_confirmed_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_confirmed_malaria_cases


class ProportionsPaludismeConsultationsTTC(IndicatorTable):
    """Graphe: Proportion des cas de paludisme par rapport aux consultations

        toutes causes confondues """

    name = u"Figure 2.1a"
    title = u""
    caption = u"Proportion des cas de paludisme par rapport aux " \
              u"consultations toutes causes confondues"
    type = 'graph'

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': False,
                       'only_percent': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0, 'total_consultation_all_causes')
    @label(u"Total consultation toutes causes confondues (TCC)")
    def total_consultation_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.total_consultation_all_causes

    @indicator(1, 'total_consultation_all_causes')
    @label(u"Consultations pour Paludisme (Tous cas suspectés)")
    def total_suspected_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_suspected_malaria_cases


class NbreCasSuspectesTestesConfirmesALL(NbreCasSuspectesTestesConfirmes):
    """ Graphe: Nombre de cas de paludisme (cas suspects, cas testés, cas

        confirmés) tout âge confondu. """

    name = u"Figure 2.2"
    caption = u"Nombre de cas de paludisme (cas suspects, " \
              u"cas testés, cas confirmés) tout âge confondu."

    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': False, \
                       'age': 'all'}


WIDGETS = [TousCasPaludismeNotifies, ProportionsPaludismeConsultationsTTC, \
           NbreCasSuspectesTestesConfirmesALL]
