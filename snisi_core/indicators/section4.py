#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


from bolibana.reporting.indicators import (IndicatorTable,
                                           reference, indicator, label)
from snisi_core.indicators.common import (get_report_for, find_report_attr_age,
                                          MalariaIndicatorTable)


class GraphDeces(IndicatorTable, MalariaIndicatorTable):
    """ Geaphe: Décès """

    name = u"Figure 5"
    title = u""
    caption = u"a"
    type = 'graph'

    default_options = {'with_percentage': False,
                       'with_total': False,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': False}

    @reference
    @indicator(0)
    @label(u"Total des décès toutes causes confondues ")
    def total_death_all_causes(self, period):
        return find_report_attr_age(self.entity, period,
                                    'total_death_all_causes',
                                    self.options.age)

    @indicator(1, "total_death_all_causes")
    @label(u"% Décès du au paludisme")
    def total_malaria_death(self, period):
        return find_report_attr_age(self.entity, period,
                                    'total_malaria_death',
                                    self.options.age)


class GraphCommun(IndicatorTable, MalariaIndicatorTable):
    """ Graphe: Evolution du nombre de décès dû au paludisme Chez les

        moins de 5 ans, les 5 ans et plus et les femmes enceintes """

    name = u"Figure 25"
    title = u""
    caption = u"Evolution du nombre de décès dû au paludisme Chez les moins " \
              u"de 5 ans, les 5 ans et plus et les femmes enceintes"
    type = 'graph'
    graph_type = 'spline'

    default_options = {'with_percentage': False,
                       'with_total': False,
                       'with_reference': False,
                       'with_data': True,
                       'only_percent': False}

    @reference
    @indicator(0)
    @label(u"Total des décès toutes causes confondues")
    def total_death_all_causes(self, period):
        report = get_report_for(self.entity, period)
        return report.total_death_all_causes

    @indicator(1, "total_death_all_causes")
    @label(u"Personnes de 5 ans et plus")
    def o5_total_malaria_death(self, period):
        report = get_report_for(self.entity, period)
        return report.o5_total_malaria_death

    @indicator(2, "total_death_all_causes")
    @label(u"Enfants de moins de 5 ans")
    def u5_total_malaria_death(self, period):
        report = get_report_for(self.entity, period)
        return report.u5_total_malaria_death

    @indicator(3, "total_death_all_causes")
    @label(u"Femmes enceintes")
    def pw_total_malaria_death(self, period):
        report = get_report_for(self.entity, period)
        return report.pw_total_malaria_death
