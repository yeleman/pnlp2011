#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.core.management.base import BaseCommand

from bolibana.models import Entity


class Command(BaseCommand):
    help = "Delete all Entity in prep for import"

    def handle(self, *args, **kwargs):

        Entity.objects.all().delete()

        print("Entities reset.")
