#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.reporting.indicators import (IndicatorTable, reference,
                                           indicator, label)
from snisi_core.indicators.common import get_report_for, MalariaIndicatorTable
from snisi_core.indicators.section4 import GraphCommun


class DecesUnderFive(IndicatorTable, MalariaIndicatorTable):
    """ Tableau: Décès notifiés chez les  moins de 5 ans """

    name = u"Tableau 13"
    title = u"Enfants moins de 5 ans"
    caption = u"Décès notifiés  pour le trimestre chez les  moins de 5 ans"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': True,
                       'with_reference': True}

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
