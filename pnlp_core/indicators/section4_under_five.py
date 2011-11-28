#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.models import Entity
from bolibana.reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label, blank)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for
from pnlp_core.indicators.section4 import GraphDeces, GraphCommun


class DecesUnderFive(IndicatorTable):
    """ Tableau: Décès notifiés chez les  moins de 5 ans """

    name = u"Tableau 13"
    title = u"Enfants moins de 5 ans"
    caption = u"Décès notifiés  pour le trimestre chez les  moins de 5 ans"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0, 'u5_total_death_all_causes')
    @label(u"Total des décès toutes causes confondues")
    def u5_total_death_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_death_all_causes

    @indicator(1, 'u5_total_death_all_causes')
    @label(u"Total des décès pour paludisme")
    def u5_total_malaria_death(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_malaria_death

WIDGETS = [DecesUnderFive, GraphCommun]
