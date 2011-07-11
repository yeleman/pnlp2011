#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from pnlp_core.models import MalariaReport
from bolibana_reporting.indicators import NoSourceData


def get_report_for(entity, period, validated=True):
    """ MalariaReport for entity and period or raise NoSourceData """
    try:
        if validated:
            return MalariaReport.validated.get(entity=entity, period=period)
        else:
            return MalariaReport.unvalidated.get(entity=entity, period=period)
    except MalariaReport.DoesNotExist:
        raise NoSourceData
