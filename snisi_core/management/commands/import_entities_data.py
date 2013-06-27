#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.core.management.base import BaseCommand

from bolibana.models import Entity, EntityType
from bolibana.tools.import_utils import UnicodeReader


def normalize_entity_name(name):
    return name.upper()


class Command(BaseCommand):
    help = "Import Entity from pnlp2011 CSV"

    def handle(self, *args, **kwargs):

        fileo = open('pnlp_entities.csv', 'r')
        csv_reader = UnicodeReader(fileo)

        Entity.objects.all().delete()

        for entity_line in csv_reader:

            old_slug, slug, name, type_slug, parent_old_slug, parents = entity_line[:6]

            try:
                parent = Entity.objects.get(slug=parent_old_slug)
            except Entity.DoesNotExist:
                parent = None

            try:
                entity = Entity.objects.get(slug=slug)
            except Entity.DoesNotExist:
                # raise ValueError("Missing Entity with slug %s" % slug)
                entity = Entity.objects.create(slug=old_slug,
                                               type=EntityType.objects.get(slug=type_slug),
                                               name=normalize_entity_name(name),
                                               parent=parent)

            print(entity)

        fileo.close()

        print("Entities complete")
