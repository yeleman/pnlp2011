#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.auth.models import ContentType

from bolibana.models.Provider import Provider
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

        # create default access
        print(u"Creating ADMIN Access…")
        admin_role = Role.objects.get(slug='admin')
        entity_cls_id = None
        # find the ID of the NUTEntity CT
        for ct in ContentType.objects.all():
            if ct.model_class() == Entity:
                entity_cls_id = ct
                break

        if not entity_cls_id:
            print(u"Unable to find %s in ContentType" % Entity)
            exit(1)

        admin_access = Access.objects.create(content_type=entity_cls_id,
                                       role=admin_role,
                                       object_id=1)

        # create default users
        print(u"Creating ADMIN User…")
        call_command("createsuperuser", username='admin',
                     email='admin@snisi.sante.gov.ml',
                     interactive=False)
        admin = User.objects.get(username='admin')
        admin.set_password('admin')
        admin.save()

        print(u"Creating autobot Provider…")
        autobot = User.objects.create_user('autobot',
                                           'autobot@snisi.sante.gov.ml')
        autobot.set_unusable_password()
        autobot.save()

        # Assign access to users
        print(u"Creating ADMIN Provider…")
        admin_p = Provider.objects.get(user=admin)
        admin_p.access.add(admin_access)
        admin_p.save()

        print(u"Creating autobot Provider…")
        autobot_p = Provider.objects.get(user=autobot)
        autobot_p.access.add(admin_access)
        autobot_p.save()
