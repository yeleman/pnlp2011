#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import time
import logging
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError

from pnlp_core.data import current_reporting_period
from pnlp_core.models import EndOfCSComPeriod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("Launching PNLP daily tasks script")

        now = datetime.now()
        period = current_reporting_period()

        for alert_cls in Alert.__subclasses__():
            # we don't want to automatically get alerts
            continue

        # if end of CSCOM period
        #   warn CSCOM which did not provide report.
        #   warn district with open report that cscom period is over.
        cscom = EndOfCSComPeriod.create(period=period)
        if cscom.can_trigger():
            logger.info("End of CSCom reporting period.")
            cscom.trigger()


        # if end of DISTRICT period
        #   validate non-validated reports.
        #   create aggregated reports
        #   warn region that district reports are available.


        # if end of REGION period
        #   validate non-validated reports.
        #   create aggregated reports.
        #   create national report.

        # send reminders:
        #   district if they have unvalidated reports and before end of period
        #   region if they have unvalidated reports and before end of period
        #   cscom if they are in sending period and have not sent

        # last day of month
        #   send SMS+email to hotline so they send units to everybody
