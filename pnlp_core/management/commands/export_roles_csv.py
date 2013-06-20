#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy

from bolibana.models import Role
from bolibana.export_utils import UnicodeWriter


class Command(BaseCommand):
    help = ugettext_lazy("Export pnlp2011 Role to CSV")

    def handle(self, *args, **kwargs):

        fileo = open('pnlp_roles.csv', 'w')
        csv_writer = UnicodeWriter(fileo)

        # Export Provider
        for role in Role.objects.all():
            data = [role.slug, "",
                    role.name,
                    role.level or "",
                    " ".join([p.slug for p in role.permissions.all()])]
            csv_writer.writerow(data)
            print(role.name)

        fileo.close()

        print("Roles complete")
