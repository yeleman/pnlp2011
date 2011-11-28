#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.models import Entity
from bolibana.reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label, blank)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for
from pnlp_core.indicators.section3 import Hospitalisation


class HospitalisationToutAgeConfondu(IndicatorTable):
    """ Tableau: Hospitalisation """
    name = u"Tableau 4.1a"
    title = u"Tout âge confondu"
    caption = u"Hospitalisation"
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
    def total_malaria_inpatient(self, period):
        report = get_report_for(self.entity, period)
        return report.total_malaria_inpatient


class ProportionHospitalisations(Hospitalisation):
    """ Graphe: Proportion des hospitalisations pour paludisme grave (par

        rapport aux hospitalisations toutes causes confondues)"""

    name = u"Figure 4.1a"
    caption = u"Proportion des hospitalisations pour paludisme grave (par" \
              u" rapport aux hospitalisations toutes causes confondues)"

    default_options = {'with_percentage': True, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': True, \
                       'age': 'all'}


WIDGETS = [HospitalisationToutAgeConfondu, ProportionHospitalisations]
