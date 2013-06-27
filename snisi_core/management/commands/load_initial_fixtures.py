#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import ContentType
from django.contrib.auth import get_user_model
from django.conf import settings

from bolibana.models.Access import Access
from bolibana.models.Role import Role
from bolibana.models.Entity import Entity


class Command(BaseCommand):

    def handle(self, *args, **options):

        # load safe fixtures
        print(u"Important safe fixtures…")
        call_command("loaddata", "fixtures/snisi/sites.Site.xml")
        call_command("loaddata", "fixtures/snisi/bolibana.Permission.xml")
        call_command("loaddata", "fixtures/snisi/bolibana.Role.xml")
        call_command("loaddata", "fixtures/snisi/bolibana.EntityType.xml")
        call_command("loaddata", "fixtures/snisi/bolibana.Entity-root.xml")
        call_command("loaddata", "fixtures/snisi/bolibana.reportclass.xml")

        # Find Entity Class ID
        entity_cls_id = None
        # find the ID of the Entity CT
        for ct in ContentType.objects.all():
            if ct.model_class() == Entity:
                entity_cls_id = ct
                break

        if not entity_cls_id:
            print(u"Unable to find %s in ContentType" % Entity)
            exit(1)

        # create default access
        print(u"Creating ADMIN Access…")
        admin_role = Role.objects.get(slug='admin')
        try:
            admin_access = Access.objects.get(role=admin_role)
        except Access.DoesNotExist:
            admin_access = Access.objects.create(content_type=entity_cls_id,
                                                 role=admin_role,
                                                 object_id=1)

        print(u"Creating Guest Access…")
        guest_role = Role.objects.get(slug='guest')
        try:
            guest_access = Access.objects.get(role=guest_role)
        except Access.DoesNotExist:
            guest_access = Access.objects.create(content_type=entity_cls_id,
                                                 role=guest_role,
                                                 object_id=1)

        # create default users
        print(u"Creating ADMIN User…")
        try:
            admin = get_user_model().objects.get(username='admin')
        except get_user_model().DoesNotExist:
            admin = get_user_model().objects.create_superuser(
                username='admin',
                email='admin@snisi.sante.gov.ml',
                password=None,
                access=admin_access)
        admin.set_password(settings.ADMIN_PASSWORD)
        admin.save()

        print(u"Creating autobot Provider…")
        try:
            autobot = get_user_model().objects.get(username='autobot')
        except get_user_model().DoesNotExist:
            autobot = get_user_model().objects.create_superuser(
                username='autobot',
                email='autobot@snisi.sante.gov.ml',
                password=None,
                access=admin_access)
        autobot.save()
