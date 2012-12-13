#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import locale
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from pnlp_core.data import current_reporting_period
from pnlp_core.alerts import (EndOfCSComPeriod, \
                                    EndOfDistrictPeriod, \
                                    MalariaReportCreated, \
                                    Reminder, EndOfMonth)
from bolibana.models import MonthPeriod
from pnlp_core.models import MalariaReport

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


class Command(BaseCommand):

    def handle(self, *args, **options):

        translation.activate(settings.DEFAULT_LOCALE)

        logger.info(u"Launching PNLP daily tasks script")

        period = current_reporting_period()

        logger.info(u"Remove orphan periods")
        [p.delete() for p 
                    in MonthPeriod.objects.all()
                    if MalariaReport.objects.filter(period=p).count() == 0]

        # if new incoming report
        report = MalariaReportCreated.create(period=period, persit=False)
        if report.can_trigger():
            logger.info(u"Incoming reports.")
            report.trigger()

        # if end of CSCOM period
        cscom = EndOfCSComPeriod.create(period=period)
        if cscom.can_trigger():
            logger.info(u"End of CSCom reporting period.")
            cscom.trigger()

        # if end of DISTRICT period
        district = EndOfDistrictPeriod.create(period=period, is_district=True)
        if district.can_trigger():
            logger.info(u"End of District reporting period.")
            district.trigger()

        # if end of REGION period
        region = EndOfDistrictPeriod.create(period=period, is_district=False)
        if region.can_trigger():
            logger.info(u"End of Region reporting period.")
            region.trigger()

        cscom_reminder = Reminder.create(period=period, level='cscom')
        if cscom_reminder.can_trigger():
            logger.info(u"CSCom reminder.")
            cscom_reminder.trigger()

        district_reminder = Reminder.create(period=period, level='district')
        if district_reminder.can_trigger():
            logger.info(u"District reminder.")
            district_reminder.trigger()

        region_reminder = Reminder.create(period=period, level='region')
        if region_reminder.can_trigger():
            logger.info(u"Region reminder.")
            region_reminder.trigger()

        # last day of month
        #   send SMS+email to hotline so they send units to everybody
        eom = EndOfMonth.create(period=period)
        if eom.can_trigger():
            logger.info(u"End of Month.")
            eom.trigger()

        translation.deactivate()
