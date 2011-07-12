#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana_reporting.models import Entity
from bolibana_reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label, blank)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for
from pnlp_core.indicators.section4 import Hospitalisation


class Hospitalisation5ansPlus(IndicatorTable):
    """ Tableau: Hospitalisation  chez les 5 ans et plus"""
    name = u"Tableau 3.2b"
    title = u"5 ans et plus"
    caption = u"Hospitalisation  chez les 5 ans et plus"
    type = 'table'

    default_options = {'with_percentage': True, \
                       'with_total': True, \
                       'with_reference': True}

    def period_is_valid(self, period):
        return MalariaReport.validated.filter(entity=self.entity, \
                                              period=period).count() > 0

    @reference
    @indicator(0)
    @label(u"Total des hospitalisations (toutes causes confondues)")
    def total_inpatient_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.total_inpatient_all_causes

    @indicator(1, 'total_inpatient_all_causes')
    @label(u"Total des hospitalisations pour paludisme grave")
    def o5_total_malaria_inpatient(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_malaria_inpatient


class ProportionHospitalisations5ansPlus(Hospitalisation):
    """ Graphe: Proportion des hospitalisations pour paludisme grave chez les

        personnes de 5 ans et plus (par rapport aux hospitalisations toutes
        causes confondues) """

    name = u"Figure 3.2b"
    caption = u"Proportion des hospitalisations pour paludisme grave chez" \
              u" les personnes de 5 ans et plus (par rapport aux " \
              u" hospitalisations toutes causes confondues)"

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True, \
                       'age': 'over_five'}

WIDGETS = [Hospitalisation5ansPlus, ProportionHospitalisations5ansPlus]
