#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import locale
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from snisi_core.data import current_reporting_period
from snisi_core.alerts import (EndOfCSComPeriod,
                               EndOfDistrictPeriod,
                               MalariaReportCreated,
                               Reminder, EndOfMonth)
from bolibana.models.Period import MonthPeriod
from snisi_core.models.MalariaReport import MalariaR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


class Command(BaseCommand):

    def handle(self, *args, **options):

        translation.activate(settings.DEFAULT_LOCALE)

        logger.info(u"Launching PNLP daily tasks script")

        period = current_reporting_period()

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
