#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy

from bolibana.models import Provider
from bolibana.export_utils import serialize_provider


class Command(BaseCommand):
    help = ugettext_lazy("Export pnlp2011 Providers to JSON")

    def handle(self, *args, **kwargs):

        items = []
        fileo = open('pnlp_users.json', 'w')

        # Export Provider
        for provider in Provider.objects.all():
            data = serialize_provider(provider)
            items.append(data)

            print(provider)

        json.dump(items, fileo)
        fileo.close()

        print("Provider complete")
