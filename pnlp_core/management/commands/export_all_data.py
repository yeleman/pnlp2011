#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Export pnlp2011 data"

    def handle(self, *args, **kwargs):
        call_command('export_entities_csv')
        call_command('export_roles_csv')
        call_command('export_providers')
        call_command('export_malariareport')
