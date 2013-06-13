#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.reporting.indicators import (IndicatorTable,
                                           reference, indicator, label)
from snisi_core.models.MalariaReport import MalariaR
from snisi_core.indicators.common import nb_stockout
from snisi_core.indicators.common import (get_report_for,
                                          get_report_for_element,
                                          get_report_national,
                                          MalariaIndicatorTable)


class CTAMILD(IndicatorTable, MalariaIndicatorTable):
    """ Tableau: Données sur la CPN et le Traitement Préventif  Intermittent

        (TPI) """

    name = u"Tableau 27"
    title = u" "
    caption = u"Pourcentage de femmes enceintes vues en CPN ayant reçu une" \
              u" MILD ou un SP2"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': True}

    @reference
    @indicator(0)
    @label(u"femmes enceintes reçues en CPN")
    def pw_total_anc1(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_anc1

    @indicator(1, 'pw_total_anc1')
    @label(u"MILD distribuées aux femmes enceintes")
    def pw_total_distributed_bednets(self, period):
        """Total des moustiquaires distribues aux femmes enceintes"""
        report = get_report_for(self.entity, period)
        return report.pw_total_distributed_bednets

    @indicator(2, 'pw_total_anc1')
    @label(u"femmes enceintes ayant reçu la SP2")
    def pw_total_sp2(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_sp2


class GrapheCTAMILD(CTAMILD):
    """ Graphe: Evolution de la  CPN1, SP1 et SP2 chez les femmes enceintes"""

    name = u"Figure 37"
    title = u" "
    caption = u"Pourcentage de femmes enceintes vues en CPN ayant reçu une" \
              u" MILD ou un SP2"
    graph_type = 'spline'
    type = 'graph'

    default_options = {'with_percentage': True,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': True}

    @indicator(0, 'pw_total_anc1')
    @label(u"% de femmes enceintes reçu en CPN ayant reçu la MILD")
    def pw_total_distributed_bednets(self, period):
        return super(GrapheCTAMILD, self).pw_total_distributed_bednets(period)

    @indicator(1, 'pw_total_anc1')
    @label(u"% de femmes enceintes reçu en CPN ayant reçu la SP2")
    def pw_total_sp2(self, period):
        return super(GrapheCTAMILD, self).pw_total_sp2(period)


class TraitesCTA(IndicatorTable, MalariaIndicatorTable):
    """ Tableau: Données sur la CPN et le Traitement Préventif  Intermittent

        (TPI) """

    name = u"Tableau 28"
    title = u" "
    caption = u"Pourcentage de cas traités par CTA"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': True}

    @reference
    @indicator(0, 'bamako_total_simple_malaria_cases')
    @label(u"cas paludisme à Bamako")
    def bamako_total_simple_malaria_cases(self, period):

        if self.entity.type.slug == 'cscom' or \
           self.entity.type.slug == 'district':
            report = get_report_for_element(get_report_national(period)
                                            .sources.validated(), 1)
            return report.total_simple_malaria_cases
        else:
            report = get_report_for_element(get_report_for(self.entity,
                                            period).sources.validated(), 1)
            return report.total_simple_malaria_cases

    @indicator(1, 'bamako_total_simple_malaria_cases')
    @label(u"% cas paludisme traités par CTA à Bamako")
    def bamako_total_treated_malaria_cases(self, period):
        if self.entity.type.slug == 'cscom' or \
           self.entity.type.slug == 'district':
            report = get_report_for_element(get_report_national(period)
                                            .sources.validated(), 1)
            print report
            return report.total_treated_malaria_cases
        else:
            report = get_report_for_element(get_report_for(self.entity,
                                            period).sources.validated(), 1)
            return report.total_treated_malaria_cases

    @reference
    @indicator(2, 'segou_total_simple_malaria_cases')
    @label(u"cas paludisme à Ségou")
    def segou_total_simple_malaria_cases(self, period):
        if self.entity.type.slug == 'cscom' or \
           self.entity.type.slug == 'district':
            report = get_report_for_element(get_report_national(period)
                                            .sources.validated(), 0)
            return report.total_simple_malaria_cases
        else:
            report = get_report_for_element(get_report_for(self.entity,
                                            period).sources.validated(), 0)
            return report.total_simple_malaria_cases

    @indicator(3, 'segou_total_simple_malaria_cases')
    @label(u"% cas paludisme traités par CTA à Ségou")
    def segou_total_treated_malaria_cases(self, period):
        if self.entity.type.slug == 'cscom' or \
           self.entity.type.slug == 'district':
            report = get_report_for_element(get_report_national(period)
                                            .sources.validated(), 0)
            return report.total_treated_malaria_cases
        else:
            report = get_report_for_element(get_report_for(self.entity,
                                            period).sources.validated(), 0)
            return report.total_treated_malaria_cases


class GrapheTraitesCTA(TraitesCTA):
    """ Graphe: Nombre de femmes enceintes reçues en CPN1 et Nombre de

        MILD distribuées aux femmes enceintes"""

    name = u"Figure 38"
    title = u" "
    caption = u"Pourcentage de cas traités par CTA"
    graph_type = 'spline'
    type = 'graph'

    default_options = {'with_percentage': True,
                       'with_reference': False,
                       'with_data': False,
                       'only_percent': True}


class PourcentageCTATDRMILD(IndicatorTable):
    """ Tableau: Pourcentage de structures avec Rupture de stock de CTA dans

        le district """

    name = u"Tableau 29"
    title = u" "
    caption = u"Pourcentage de structures sans Rupture de stock de CTA, " \
              u"TDR et MILD"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': True}

    def period_is_valid(self, period):
        return True

    @reference
    @indicator(0)
    @label(u"Nombre total de structures dans le district")
    def total_structures_in_the_district(self, period):
        if self.entity.type.slug == 'cscom':
            return 1
        else:
            return self.entity.get_descendants()\
                              .filter(type__slug='cscom').count()

    @indicator(1, 'total_structures_in_the_district')
    @label(u"CTA")
    def stockout_act(self, period):
        nb_stockout_CTA = 0
        for report in MalariaR.objects.filter(type=MalariaR.TYPE_SOURCE,
                                              period=period):
            if (getattr(report, 'stockout_act_children') == report.NO
                and (self.entity in report.entity.get_ancestors()
                or self.entity == report.entity)) \
                or (getattr(report, 'stockout_act_youth') == report.NO
                    and (self.entity in report.entity.get_ancestors()
                    or self.entity == report.entity)) \
                    or (getattr(report, 'stockout_act_adult') == report.NO
                        and (self.entity in report.entity.get_ancestors()
                        or self.entity == report.entity)):
                nb_stockout_CTA += 1
        return nb_stockout_CTA

    @indicator(2, 'total_structures_in_the_district')
    @label(u"TDR")
    def stockout_rdt(self, period):
        nb_rdt = nb_stockout(self.entity, period, 'rdt')
        return nb_rdt

    @indicator(3, 'total_structures_in_the_district')
    @label(u"MILD")
    def stockout_bednet(self, period):
        nb_bednet = nb_stockout(self.entity, period, 'bednet')
        return nb_bednet


class GraphePourcentageCTATDRMILD(PourcentageCTATDRMILD):
    """ Graphe: Nombre de femmes enceintes reçues en CPN1 et Nombre de

        MILD distribuées aux femmes enceintes"""

    name = u"Figure 39"
    title = u" "
    caption = u"Pourcentage de structures sans Rupture de stock de CTA, " \
              u"TDR et MILD"
    graph_type = 'spline'
    type = 'graph'

    default_options = {'with_percentage': True,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': True}

    @indicator(0, 'total_structures_in_the_district')
    @label(u"% de structures sans Rupture de stock de CTA")
    def stockout_act(self, period):
        return super(GraphePourcentageCTATDRMILD, self).stockout_act(period)

    @indicator(1, 'total_structures_in_the_district')
    @label(u"% de structures sans Rupture de stock de TDR")
    def stockout_rdt(self, period):
        return super(GraphePourcentageCTATDRMILD, self).stockout_rdt(period)

    @indicator(2, 'total_structures_in_the_district')
    @label(u"% de structures sans Rupture de stock de MILD")
    def stockout_bednet(self, period):
        return super(GraphePourcentageCTATDRMILD, self).stockout_bednet(period)

WIDGETS = [CTAMILD, GrapheCTAMILD, TraitesCTA,
           GrapheTraitesCTA, PourcentageCTATDRMILD,
           GraphePourcentageCTATDRMILD]
