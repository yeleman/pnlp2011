#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana_reporting.models import Entity
from bolibana_reporting.indicators import (IndicatorTable, NoSourceData, \
                                           reference, indicator, label, blank)
from pnlp_core.models import MalariaReport
from pnlp_core.data import current_reporting_period
from pnlp_core.indicators.common import get_report_for
from pnlp_core.indicators.section2 import NbreCasSuspectesTestesConfirmes


class NbreCasSuspectesTestesConfirmesO5(NbreCasSuspectesTestesConfirmes):

    name = u"Figure 2.2b"
    caption = u"Nombre de cas de paludisme (cas suspects, cas testés, " \
              u"cas confirmés) chez les personnes de 5 ans et plus."

    default_options = {'with_percentage': False, \
                       'with_total': False, \
                       'with_reference': False, \
                       'with_data': True,
                       'only_percent': False, \
                       'age': 'under_five'}

WIDGETS = [NbreCasSuspectesTestesConfirmesO5]
