#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.reporting.indicators import (IndicatorTable, \
                                           reference, indicator, label)
from pnlp_core.models import MalariaReport
from pnlp_core.indicators.common import get_report_for
from pnlp_core.indicators.section4 import GraphDeces, GraphCommun


class DecesToutAgeConfondu(IndicatorTable):
    """Tableau: Décès"""

    name = u"Tableau 12"
    title = u"Tout âge confondu"
    caption = u"Décès"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Total des décès toutes causes confondues")
    def total_death_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.total_death_all_causes

    @indicator(1, 'total_death_all_causes')
    @label(u"Total des décès pour paludisme")
    def total_malaria_death(self, period):
        report = get_report_for(self.entity, period)
        return report.total_malaria_death


class ProportionDecesToutAgeConfondu(GraphDeces):
    """ Graphe: Proportion de décès dû au  paludisme (par rapport aux

        décès toutes causes confondues) """
    name = u"Figure 24"
    caption = u"Proportion de décès dû au  paludisme (par rapport aux " \
              u"décès toutes causes confondues) "

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True, \
                       'age': 'all'}


WIDGETS = [DecesToutAgeConfondu, ProportionDecesToutAgeConfondu, GraphCommun]
