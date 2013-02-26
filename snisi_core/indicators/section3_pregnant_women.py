#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.reporting.indicators import (IndicatorTable,
                                           reference, indicator, label)

from snisi_core.indicators.common import get_report_for, MalariaIndicatorTable
from snisi_core.indicators.section3 import Hospitalisation


class HospitalisationFemmesEnceintes(IndicatorTable, MalariaIndicatorTable):
    """ Tableau: Hospitalisation chez les femmes enceintes """

    name = u"Tableau 4.1d"
    title = u"Femmes enceintes"
    caption = u"Hospitalisation chez les femmes enceintes"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': True,
                       'with_reference': True}

    @reference
    @indicator(0, 'pw_total_inpatient_all_causes')
    @label(u"Total des hospitalisations (toutes causes confondues)")
    def pw_total_inpatient_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_inpatient_all_causes

    @indicator(1, 'pw_total_inpatient_all_causes')
    @label(u"Total des hospitalisations pour paludisme grave")
    def pw_total_malaria_inpatient(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_malaria_inpatient


class ProportionHospitalisationsFemmesEnceintes(Hospitalisation):
    """ Graphe: Proportion des hospitalisations pour paludisme grave chez les

        femmes enceintes (par rapport aux hospitalisations toutes causes
        confondues """
    name = u"Figure 4.1d"
    caption = (u"Proportion des hospitalisations pour paludisme grave chez"
               u" les femmes enceintes (par rapport aux hospitalisations"
               u" toutes causes confondues)")

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': True,
                       'age': 'pregnant_women'}

WIDGETS = [HospitalisationFemmesEnceintes,
           ProportionHospitalisationsFemmesEnceintes]
