#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


from bolibana.reporting.indicators import (IndicatorTable, \
                                           reference, indicator, label)
from pnlp_core.models import MalariaReport
from pnlp_core.indicators.common import find_report_attr_age


class Hospitalisation(IndicatorTable):
    """ Graphe: Hospitalisation """

    name = u"Figure 4"
    title = u""
    caption = u"Hospitalisation"
    type = 'graph'

    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': False,
                       'only_percent': False}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Total des hospitalisations (toutes causes confondues)")
    def total_inpatient_all_causes(self, period):
        return find_report_attr_age(self.entity, period, \
                               'total_inpatient_all_causes', \
                               self.options.age)

    @indicator(1, "total_inpatient_all_causes")
    @label(u"Total des hospitalisations pour paludisme grave")
    def total_malaria_inpatient(self, period):
      return find_report_attr_age(self.entity, period, \
                               'total_malaria_inpatient', \
                               self.options.age)


WIDGETS = []
