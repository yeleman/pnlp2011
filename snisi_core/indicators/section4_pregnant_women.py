#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.reporting.indicators import (IndicatorTable, \
                                           reference, indicator, label)
from snisi_core.models import MalariaReport
from snisi_core.indicators.common import get_report_for
from snisi_core.indicators.section4 import GraphCommun


class DecesFemmesEnceintes(IndicatorTable):
    """ Décès notifiés chez les femmes enceintes """

    name = u"Tableau 15"
    title = u"Femmes enceintes"
    caption = u"Décès notifiés chez les femmes enceintes"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0, 'pw_total_death_all_causes')
    @label(u"Total des décès toutes causes confondues")
    def pw_total_death_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_death_all_causes

    @indicator(1, 'pw_total_death_all_causes')
    @label(u"Total des décès pour paludisme")
    def pw_total_malaria_death(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_malaria_death

WIDGETS = [DecesFemmesEnceintes, GraphCommun]
