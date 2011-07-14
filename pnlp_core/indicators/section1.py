#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.utils.translation import ugettext as _

from bolibana_reporting.models import Entity
from bolibana_reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label, blank)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for


class TableauSection1(IndicatorTable):
    name = _(u" ")
    title = _(u" ")
    caption = _(u" ")
    type = 'table'

    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': False}

    def period_is_valid(self, period):
        return True

    @indicator(0)
    @label(u"Structures")
    def total_structures_in_the_district(self, period):
        return self.entity.children.count()

    @indicator(1)
    @label(u"Auto-validation")
    def number_autovalide(self, period):
        if self.entity.type.slug == 'cscom':
            children = [self.entity]
        else:
            children = self.entity.get_descendants()
        return MalariaReport.validated.filter(entity__in=children, \
            modified_by__user__username='autobot').count()

    @indicator(2)
    @label(u"Total rapports")
    def number_tautovalide(self, period):
        return self.entity.reports.count()

    #~ @indicator(2, 'total_structures_in_the_district')
    #~ @label(u"SMS")
    #~ def number_sms(self, period):
        #~ children = self.entity.get_children()
        #~ sms = 0
        #~ for source in self.entity.sources.all():
            #~ if source.created_by.first_role() == 'cscom':
                #~ sms += 1
        #~ return report.sources.filter(created_by)

WIDGETS = [TableauSection1(IndicatorTable]
