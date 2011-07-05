#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import time
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from pnlp_core.data import current_reporting_period
from pnlp_core.models.alert import (EndOfCSComPeriod, \
                                    EndOfDistrictPeriod, \
                                    MalariaReportCreated)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

        # send reminders:
        #   district if they have unvalidated reports and before end of period
        #   region if they have unvalidated reports and before end of period
        #   cscom if they are in sending period and have not sent

        # last day of month
        #   send SMS+email to hotline so they send units to everybody
