#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy

from bolibana.models import Entity
from bolibana.export_utils import UnicodeWriter
from pnlp_core.models import MalariaReport


def entity_is_used(entity):
    return MalariaReport.objects.filter(entity=entity).count()


class Command(BaseCommand):
    help = ugettext_lazy("Export pnlp2011 Entity to CSV")

    def handle(self, *args, **kwargs):

        fileo = open('pnlp_entities.csv', 'w')
        csv_writer = UnicodeWriter(fileo)

        # Export Provider
        for entity in Entity.objects.all():

            # don't waste time double codifying non-used locations
            if not entity_is_used(entity):
                continue

            data = [entity.slug, "",
                    entity.display_name(), entity.type.slug,
                    "/".join([e.display_name() for e in entity.get_ancestors()[1:]])]
            csv_writer.writerow(data)
            print(entity.display_full_name())

        fileo.close()

        print("Entities complete")
