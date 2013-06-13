#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.reporting.indicators import (IndicatorTable,
                                           reference, indicator, label, hidden)
from snisi_core.indicators.common import (get_report_national, get_report_for,
                                          get_report_for_element,
                                          MalariaIndicatorTable)


class CasConfirmes(IndicatorTable, MalariaIndicatorTable):
    """ """

    name = u"Tableau 21"
    title = u" "
    caption = u"Pourcentage de cas de paludisme confirmés chez les moins" \
              u" de 5 ans et tout âge confondu"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': True}

    @reference
    @indicator(0, 'u5_total_tested_malaria_cases')
    @label(u"Total des cas suspects testés chez les moins de 5 ans")
    def u5_total_tested_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_tested_malaria_cases

    @indicator(1, 'u5_total_tested_malaria_cases')
    @label(u"Total des cas confirmés chez les moins de 5 ans")
    def u5_total_confirmed_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_confirmed_malaria_cases

    @reference
    @indicator(2, 'total_tested_malaria_cases')
    @label(u"Total des cas suspects testés chez Tout âge confondu")
    def total_tested_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_tested_malaria_cases

    @indicator(3, 'total_tested_malaria_cases')
    @label(u"Total des cas confirmés chez Tout âge confondu")
    def total_confirmed_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_confirmed_malaria_cases


class GrapheConfirmes(CasConfirmes):
    """ Graphe: Pourcentage de cas de paludisme confirmés chez les moins de 5

        ans et tout âge confondu """

    name = u"Figure 31"
    caption = u"Pourcentage de cas de paludisme confirmés chez les moins" \
              u" de 5 ans et tout âge confondu"
    graph_type = 'spline'
    type = "graph"
    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': True}

    @indicator(0, 'u5_total_tested_malaria_cases')
    @label(u"% des cas confirmés chez les moins de 5 ans")
    def u5_total_confirmed_malaria_cases(self, period):
        return super(GrapheConfirmes, self).u5_total_confirmed_malaria_cases(period)

    @indicator(1, 'total_tested_malaria_cases')
    @label(u"% des cas confirmés chez Tout âge confondu")
    def total_confirmed_malaria_cases(self, period):
        return super(GrapheConfirmes, self).total_confirmed_malaria_cases(period)


class NbreHospitalisationDeces(IndicatorTable, MalariaIndicatorTable):
    """ Tableau: Données sur l'hospitalisation et le decès pour paludisme chez

        les moins de 5 ans """

    name = u"Tableau 22"
    title = u"Nombre d'hospitalisation et décès pour paludisme chez les moins 5 ans"
    caption = u"Nombre d'hospitalisation et décès pour paludisme chez les moins 5 ans"
    type = 'table'

    default_options = {'with_percentage': False,
                       'with_total': False,
                       'with_reference': True}

    @indicator(0)
    @label(u"hospitalisations pour paludisme")
    def u5_total_malaria_inpatient(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_malaria_inpatient

    @indicator(1)
    @label(u"Décès pour paludisme")
    def u5_total_malaria_death(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_malaria_death


class GrapheNbreHospitalisationDeces(NbreHospitalisationDeces):
    """ Graphe: Données sur l'hospitalisation et le decès pour paludisme chez

        les moins de 5 ans """

    name = u"Figure 32"
    title = u" "
    caption = u"Nombre d'hospitalisation et décès pour paludisme chez les" \
              u" moins de 5 ans"
    type = 'graph'
    graph_type = 'spline'

    default_options = {'with_percentage': False,
                       'with_reference': False,
                       'with_data': False,
                       'only_percent': False}


class DecesPaluToutCauses(IndicatorTable, MalariaIndicatorTable):
    """ Tableau: Données de décès pour paludisme et toutes causes chez les

        moins de 5 ans """

    name = u"Tableau 23"
    title = u" "
    caption = u"Pourcentage de décès pour paludisme et pourcentage de décès " \
              u"toutes causes chez les moins de 5 ans"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': True}

    @reference
    @indicator(0, 'u5_total_consultation_all_causes')
    @label(u"Total consultation chez les moins de 5 ans")
    def u5_total_consultation_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_consultation_all_causes

    @indicator(1, 'u5_total_consultation_all_causes')
    @label(u"décès toutes causes confondues chez les moins de 5 ans")
    def u5_total_death_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_death_all_causes

    @indicator(2, 'u5_total_death_all_causes')
    @label(u"décès pour paludisme chez les moins de 5 ans")
    def u5_total_malaria_death(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_malaria_death

    @reference
    @indicator(3, 'o5_total_consultation_all_causes')
    @label(u"Total consultation chez les 5 ans et plus")
    def o5_total_consultation_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_consultation_all_causes

    @indicator(4, 'o5_total_consultation_all_causes')
    @label(u"décès toutes causes confondues chez les 5 ans et plus")
    def o5_total_death_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_death_all_causes

    @indicator(5, 'o5_total_death_all_causes')
    @label(u"décès pour paludisme chez les 5 ans et plus")
    def o5_total_malaria_death(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_malaria_death


class GrapheDecesPaluToutCauses(DecesPaluToutCauses):
    """ Graphe: Pourcentage de décès pour paludisme et toutes causes chez les

        moins de 5 ans """

    name = u"Figure 33"
    title = u" "
    caption = u"Pourcentage de décès pour paludisme et pourcentage de décès " \
              u"toutes causes chez les moins de 5 ans"
    graph_type = 'spline'
    type = 'graph'

    default_options = {'with_percentage': True,
                       'with_reference': False,
                       'with_data': False,
                       'only_percent': True}

    @hidden
    @indicator(0, 'u5_total_consultation_all_causes')
    @label(u"% décès toutes causes confondues chez les moins de 5 ans")
    def u5_total_death_all_causes(self, period):
        return super(GrapheDecesPaluToutCauses,
                     self).u5_total_death_all_causes(period)

    @indicator(1, 'u5_total_death_all_causes')
    @label(u"% décès pour paludisme chez les moins de 5 ans")
    def u5_total_malaria_death(self, period):
        return super(GrapheDecesPaluToutCauses,
                     self).u5_total_malaria_death(period)

    @hidden
    @indicator(2, 'o5_total_consultation_all_causes')
    @label(u"% décès toutes causes confondues chez les 5 ans et plus")
    def o5_total_death_all_causes(self, period):
        return super(GrapheDecesPaluToutCauses,
                     self).o5_total_death_all_causes(period)

    @indicator(3, 'o5_total_death_all_causes')
    @label(u"% décès pour paludisme chez les 5 ans et plus")
    def o5_total_malaria_death(self, period):
        return super(GrapheDecesPaluToutCauses,
                     self).o5_total_malaria_death(period)


class DecesPalu(IndicatorTable):
    """ Tableau: Pourcentage de decès pour paludisme chez les moins de

        5 ans """

    name = u"Tableau 24"
    title = u" "
    caption = u"Pourcentage de decès pour paludisme chez les moins de 5 ans" \
              u" Bamako/Segou"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': True}

    def period_is_valid(self, period):
        return True

    @reference
    @indicator(0, 'bamako_total_malaria_death')
    @label(u"Total décès pour paludisme à Bamako")
    def bamako_total_malaria_death(self, period):
        if self.entity.type.slug == 'cscom' or \
           self.entity.type.slug == 'district':
            report = get_report_for_element(get_report_national(period)
                                            .sources.validated(), 1)
            print report
            return report.total_malaria_death
        else:
            report = get_report_for_element(get_report_for(self.entity,
                                            period).sources.validated(), 1)
            return report.total_malaria_death

    @indicator(1, 'bamako_total_malaria_death')
    @label(u"Décès pour paludisme chez les 5 ans à Bamako")
    def bamako_u5_total_malaria_death(self, period):

        if self.entity.type.slug == 'cscom' or \
           self.entity.type.slug == 'district':
            report = get_report_for_element(get_report_national(period)
                                            .sources.validated(), 1)
            return report.u5_total_malaria_death
        else:
            report = get_report_for_element(get_report_for(self.entity,
                                            period).sources.validated(), 1)
            return report.u5_total_malaria_death

    @reference
    @indicator(2, 'segou_total_malaria_death')
    @label(u"Total décès pour paludisme à Ségou")
    def segou_total_malaria_death(self, period):
        if self.entity.type.slug == 'cscom' or \
           self.entity.type.slug == 'district':
            report = get_report_for_element(get_report_national(period)
                                            .sources.validated(), 0)
            return report.total_malaria_death
        else:
            report = get_report_for_element(get_report_for(self.entity,
                                            period).sources.validated(), 0)
            return report.total_malaria_death

    @indicator(3, 'segou_total_malaria_death')
    @label(u"Décès pour paludisme chez les 5 ans à Ségou")
    def segou_u5_total_malaria_death(self, period):
        if (self.entity.type.slug == 'cscom'
           or self.entity.type.slug == 'district'):
            report = get_report_for_element(get_report_national(period)
                                            .sources.validated(), 0)
            return report.u5_total_malaria_death
        else:
            report = get_report_for_element(get_report_for(self.entity,
                                            period).sources.validated(), 0)
            return report.u5_total_malaria_death


class GrapheDecesPalu(DecesPalu):
    """ Graphe: Pourcentage de decès pour paludisme chez les moins de 5 ans """

    name = u"Figure 34"
    title = u" "
    caption = u"Pourcentage de decès pour paludisme chez les moins de 5 ans"
    graph_type = 'spline'
    type = 'graph'

    default_options = {'with_percentage': True,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': True}

    @indicator(0, 'bamako_total_malaria_death')
    @label(u"% décès pour paludisme chez les 5 ans à Bamako")
    def bamako_u5_total_malaria_death(self, period):
        return super(GrapheDecesPalu, self).bamako_u5_total_malaria_death(period)

    @indicator(1, 'segou_total_malaria_death')
    @label(u"% décès pour paludisme chez les 5 ans à Ségou")
    def segou_u5_total_malaria_death(self, period):
        return super(GrapheDecesPalu, self).segou_u5_total_malaria_death(period)


class CasTestesConfirmes(IndicatorTable, MalariaIndicatorTable):
    """ Tableau: Pourcentage de cas de suspect testés et pourcentage de cas de

        paludisme confirmés parmi les cas testés """

    name = u"Tableau 25"
    title = u" "
    caption = u"Pourcentage de cas suspect testés et pourcentage de cas de " \
              u"paludisme confirmés parmi les cas testés"
    type = 'table'

    default_options = {'with_percentage': True,
                       'with_total': False,
                       'with_reference': True}

    @reference
    @indicator(0)
    @label(u"Total des cas suspects")
    def total_suspected_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_suspected_malaria_cases

    @indicator(1, 'total_suspected_malaria_cases')
    @label(u"Total des cas suspects testés")
    def total_tested_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_tested_malaria_cases

    @indicator(2, 'total_tested_malaria_cases')
    @label(u"cas confirmés")
    def total_confirmed_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_confirmed_malaria_cases


class GrapheCasTestesConfirmes(CasTestesConfirmes):
    """ Graphe: Nombre de femmes enceintes reçues en CPN1 et Nombre de

        MILD distribuées aux femmes enceintes"""

    name = u"Figure 35"
    title = u" "
    caption = u"Pourcentage de cas suspect testés et pourcentage de cas de" \
              u" paludisme confirmés parmi les cas testés"
    graph_type = 'spline'
    type = 'graph'

    default_options = {'with_percentage': True,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': True}

    @indicator(0)
    @label(u"% des cas suspects testés")
    def total_tested_malaria_cases(self, period):
        return super(GrapheCasTestesConfirmes, self).total_tested_malaria_cases(period)

    @indicator(1, 'total_tested_malaria_cases')
    @label(u"% cas confirmés")
    def total_confirmed_malaria_cases(self, period):
        return super(GrapheCasTestesConfirmes, self).total_confirmed_malaria_cases(period)


class NbreConsultationCasSuspect(IndicatorTable, MalariaIndicatorTable):
    """ Tableau: Pourcentage de cas de suspect testés et pourcentage de cas de

        paludisme confirmés parmi les cas testés """

    name = u"Tableau 26"
    title = u" "
    caption = u"Nombre de consultation toutes causes confondues et nombre de"\
              u" cas suspects de paludisme"
    type = 'table'

    default_options = {'with_percentage': False,
                       'with_total': False,
                       'with_reference': True}

    @indicator(0, 'total_suspected_malaria_cases')
    @label(u"Total consultation(toutes causes)")
    def total_consultation_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.total_consultation_all_causes

    @indicator(1)
    @label(u"cas suspects de paludisme")
    def total_suspected_malaria_cases(self, period):
        report = get_report_for(self.entity, period)
        return report.total_tested_malaria_cases


class GrapheNbreConsultationCasSuspect(NbreConsultationCasSuspect):
    """ Graphe: Nombre de femmes enceintes reçues en CPN1 et Nombre de

        MILD distribuées aux femmes enceintes"""

    name = u"Figure 36"
    title = u" "
    caption = u"Nombre de consultation toutes causes confondues et nombre de"\
              u" cas suspects de paludisme"
    graph_type = 'spline'
    type = 'graph'

    default_options = {'with_percentage': False,
                       'with_reference': False,
                       'with_data': False,
                       'only_percent': False}


WIDGETS = [CasConfirmes, GrapheConfirmes, NbreHospitalisationDeces,
           GrapheNbreHospitalisationDeces, DecesPaluToutCauses,
           GrapheDecesPaluToutCauses,
           DecesPalu, GrapheDecesPalu, CasTestesConfirmes,
           GrapheCasTestesConfirmes, NbreConsultationCasSuspect,
           GrapheNbreConsultationCasSuspect]
