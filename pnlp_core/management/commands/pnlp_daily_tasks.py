#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import locale
import time
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from pnlp_core.data import current_reporting_period
from pnlp_core.alerts import (EndOfCSComPeriod, \
                                    EndOfDistrictPeriod, \
                                    MalariaReportCreated, \
                                    Reminder, EndOfMonth)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("Launching PNLP daily tasks script")

        now = datetime.now()
        period = current_reporting_period()

        # if new incoming report
        report = MalariaReportCreated.create(period=period, persit=False)
        if report.can_trigger():
            logger.info("Incoming reports.")
            report.trigger()

        # if end of CSCOM period
        cscom = EndOfCSComPeriod.create(period=period)
        if cscom.can_trigger():
            logger.info("End of CSCom reporting period.")
            cscom.trigger()

        # if end of DISTRICT period
        district = EndOfDistrictPeriod.create(period=period, is_district=True)
        if district.can_trigger():
            logger.info("End of District reporting period.")
            district.trigger()

        # if end of REGION period
        region = EndOfDistrictPeriod.create(period=period, is_district=False)
        if region.can_trigger():
            logger.info("End of Region reporting period.")
            region.trigger()

        cscom_reminder = Reminder.create(period=period, level='cscom')
        if cscom_reminder.can_trigger():
            logger.info("CSCom reminder.")
            cscom_reminder.trigger()

        district_reminder = Reminder.create(period=period, level='district')
        if district_reminder.can_trigger():
            logger.info("District reminder.")
            district_reminder.trigger()

        region_reminder = Reminder.create(period=period, level='region')
        if region_reminder.can_trigger():
            logger.info("Region reminder.")
            region_reminder.trigger()

        # last day of month
        #   send SMS+email to hotline so they send units to everybody
        eom = EndOfMonth.create(period=period)
        if eom.can_trigger():
            logger.info("End of Month.")
            eom.trigger()
