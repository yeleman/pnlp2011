#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from bolibana.models import Entity, EntityType, Period, Project
from bolibana.admin import EntityAdmin, EntityTypeAdmin, PeriodAdmin
from bolibana.models import Role, Permission, Access, Provider
from bolibana.admin import (RoleAdmin, PermissionAdmin, \
                                 AccessAdmin, ProviderAdmin)
from snisi_core.models import (MalariaReport, MaternalMortalityReport,
                                RHCommoditiesReport,
                                ChildrenMortalityReport,
                                EpidemiologyReport, AggregatedMalariaReport,
                                AggregatedRHCommoditiesReport,
                                AggregatedChildrenMortalityReport,
                                AggregatedMaternalMortalityReport)
from snisi_core.models.alert import Alert
from snisi_core.admin import MalariaReportAdmin, AlertAdmin


class ProviderUserStacked(admin.StackedInline):
    model = Provider
    fk_name = 'user'
    max_num = 1


class CustomUserAdmin(UserAdmin):
    inlines = [ProviderUserStacked, ]

# Adds a provider section to the django User Admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Period, PeriodAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(EntityType, EntityTypeAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Access, AccessAdmin)
admin.site.register(Permission, PermissionAdmin)

admin.site.register(MalariaReport, MalariaReportAdmin)
admin.site.register(AggregatedMalariaReport)
admin.site.register(Alert, AlertAdmin)
admin.site.register(MaternalMortalityReport)
admin.site.register(AggregatedMaternalMortalityReport)
admin.site.register(ChildrenMortalityReport)
admin.site.register(AggregatedChildrenMortalityReport)
admin.site.register(RHCommoditiesReport)
admin.site.register(AggregatedRHCommoditiesReport)
admin.site.register(EpidemiologyReport)
admin.site.register(Project)
