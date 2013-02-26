#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.reporting.indicators import (IndicatorTable,
                                           reference, indicator, label)
from snisi_core.indicators.common import get_report_for, MalariaIndicatorTable
from snisi_core.indicators.section4 import GraphCommun


class DecesOverFive(IndicatorTable, MalariaIndicatorTable):
    """ Tableau: Décès notifiés chez les 5 ans et plus """

    name = u"Tableau 14"
    title = u"5 ans et plus"
    caption = u"Décès notifiés pour le trimestre chez les 5 ans et plus"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': True,
                       'with_reference': True}

    @reference
    @indicator(0, 'o5_total_death_all_causes')
    @label(u"Total des décès toutes causes confondues")
    def o5_total_death_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_death_all_causes

    @indicator(1, 'o5_total_death_all_causes')
    @label(u"Total des décès pour paludisme")
    def o5_total_malaria_death(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_malaria_death

WIDGETS = [DecesOverFive, GraphCommun]
