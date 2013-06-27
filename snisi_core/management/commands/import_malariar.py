#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json
import reversion

from django.core.management.base import BaseCommand

from snisi_core.models.MalariaReport import MalariaR
from bolibana.tools.import_utils import (period_from, datetime_from,
                                         get_provider_from, entity_from,
                                         get_user_from)


def report_from(receipt):
    return MalariaR.objects.get(receipt=receipt)


def deserialize_malaria(report_data, report):

    def update_sources(report_data, report):

        report.sources.empty()
        for source_receipt in report_data.get('sources'):
            report.sources.add(report_from(source_receipt))
        report.save()

        return report

    def deserialize(report_data, report):

        for field, field_data in report_data.items():

            # data fields
            if field.split('_')[0] in ('u5', 'o5', 'pw', 'stockout') \
               or field in ('receipt', '_status', 'type'):
                setattr(report, field, field_data)

            # datetimes
            if field in ('created_on', 'modified_on'):
                setattr(report, field, datetime_from(report_data.get(field)))

            # period
            if field == 'period':
                setattr(report, field, period_from(report_data.get(field)))

            # providers
            if field in ('created_by', 'modified_by'):
                setattr(report, field, get_provider_from(report_data.get(field)))

            # entity
            if field == 'entity':
                setattr(report, field, entity_from(report_data.get(field)))

    report = deserialize(report_data, report)
    report.save()
    report = update_sources(report_data, report)
    return report


def update_last_revision(report, revision):
    version = reversion.get_unique_for_object(report).pop()
    version.revision.date_created = datetime_from(revision.get('date'))
    version.revision.user = get_user_from(revision.get('user'))
    version.save()


class Command(BaseCommand):

    help = "Import MalariaR from pnlp2011 JSON"

    def handle(self, *args, **kwargs):

        report_list = json.load(open('pnlp_malaria_reports.json', 'r'))

        for report_data in report_list:

            from pprint import pprint as pp ; pp(report_data)

            report = MalariaR()
            report = deserialize_malaria(report_data, report)
            with reversion.create_revision():
                report.save()
                reversion.set_comment("Original version - SNISI import")
            update_last_revision(report, report_data.get('_version'))

            for update in report_data.get('updates'):
                report = deserialize_malaria(update, report)
                with reversion.create_revision():
                    report.save()
                    reversion.set_comment("Update - SNISI import")
                update_last_revision(report, update.get('_version'))

            break

        print("MalariaR imported.")
