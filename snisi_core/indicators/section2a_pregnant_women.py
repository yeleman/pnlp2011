#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


from bolibana.reporting.indicators import (IndicatorTable, reference,
                                           indicator, label)
from snisi_core.indicators.common import get_report_for, MalariaIndicatorTable
from snisi_core.indicators.section2 import (NbreCasSuspectesTestesConfirmes,
                                            CasTestes, CasConfirmes)


class CasPaludismeFemmesEnceintes(IndicatorTable, MalariaIndicatorTable):
    """ Tableau: Nombre de cas de paludisme chez les femmes enceintes """

    name = u"Tableau 6"
    title = u"Femmes enceintes"
    caption = u"Nombre de cas de paludisme chez les femmes enceintes"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': True,
                       'with_reference': True}

    @reference
    @indicator(0, 'pw_total_suspected_malaria_cases')
    @label(u"Nombre de cas de paludisme (tous suspectés)")
    def pw_total_suspected_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_suspected_malaria_cases

    @indicator(1, 'pw_total_suspected_malaria_cases')
    @label(u"Total des cas suspects testés (GE et/ou TDR)")
    def pw_total_tested_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_tested_malaria_cases

    @label(u"Nombre de cas suspects testés qui sont confirmés par"
           u" GE ou TDR(cas graves)")
    @indicator(2, 'pw_total_tested_malaria_cases')
    def pw_total_severe_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_severe_malaria_cases


class NbreTestesConfirmesFemmesEnceintes(NbreCasSuspectesTestesConfirmes):
    """ Nombre de cas de paludisme  par mois (cas suspects,

        cas testés,  cas confirmés)  chez les femmes enceintes. """

    name = u"Figure 14"
    caption = u"Nombre de cas de paludisme  par mois (cas suspects," \
              u"cas testés,  cas confirmés)  chez les femmes enceintes."

    default_options = {'with_percentage': False,
                       'with_total': False,
                       'with_reference': True,
                       'with_data': True,
                       'only_percent': False,
                       'age': 'pregnant_women'}


class EvolutionTestesFemmesEnceintes(CasTestes):
    """ Graphe: Evolution de la proportion des cas testés parmi les

        cas suspects chez les femmes enceintes. """

    name = u"Figure 15"
    caption = u"Evolution de la proportion des cas testés parmi les" \
              u"cas suspects chez les femmes enceintes. "
    graph_type = 'spline'
    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': True,
                       'age': 'pregnant_women'}


class EvolutionConfirmesFemmesEnceintes(CasConfirmes):
    """ Graphe: Evolution de la proportion des cas confirmés parmi

        les cas testés  chez les femmes enceintes. """

    name = u"Figure 16"
    caption = u"Evolution de la proportion des cas confirmés parmi " \
              u"les cas testés  chez les femmes enceintes"
    graph_type = 'spline'
    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': True,
                       'age': 'pregnant_women'}
WIDGETS = [CasPaludismeFemmesEnceintes,
           NbreTestesConfirmesFemmesEnceintes,
           EvolutionTestesFemmesEnceintes,
           EvolutionConfirmesFemmesEnceintes]
