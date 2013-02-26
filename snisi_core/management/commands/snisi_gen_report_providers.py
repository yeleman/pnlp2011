#!/usr/bin/env python
# encoding=utf-8

import logging
from datetime import date, timedelta

from optparse import make_option
from django.core.management.base import BaseCommand

from bolibana.models.ExpectedReporting import ExpectedReporting
from bolibana.models.ScheduledReporting import ScheduledReporting

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generating_for(day):

    logger.info("Generating Expected Reportings: %s" % day)

    def get_period_for(period_cls):

        periods = {}

        if periods.get(period_cls):
            return periods.get(period_cls)
        else:
            period = period_cls.find_create_by_date(day, dont_create=True)
            periods.update({period_cls: period})
            return period

    # loop on ScheduledReporting
    for scheduled_reporting in ScheduledReporting.objects.all():

        # Period Type for the reportclass
        period_cls = scheduled_reporting.report_class.period_class

        # Period of the previous type for now
        period = get_period_for(period_cls)

        # shortcut to start of schedule in appropriate type
        start = scheduled_reporting.casted_start

        # shortcut to start of schedule in appropriate type
        end = scheduled_reporting.casted_end

        expr, created = ExpectedReporting.objects.get_or_create(
                             report_class=scheduled_reporting.report_class,
                             entity=scheduled_reporting.entity,
                             period=period,
                             level=scheduled_reporting.level)

        if start is not None and period >= start \
            and (period < end or end is None):
            # We need to have one for the period.
            # It might already exist though.
            if created:
                logger.info("Created %s" % expr)
        else:
            expr.delete()
            if not created:
                logger.info("Removed %s" % expr)



class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--from',
            help='Create Expected from a fixed date',
            default=False),)


    def handle(self, *args, **options):

        today = date.today()
        try:
            start_from = date(*[int(x)
                                for x in options.get('from').split('-')])
        except:
            start_from = None

        if start_from:
            day = start_from
            while day <= today:
                generating_for(day)
                day += timedelta(1)
        else:
            generating_for(today)
