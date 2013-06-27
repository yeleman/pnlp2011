#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import admin

from bolibana.models.Entity import Entity
from bolibana.models.ReportClass import ReportClass
from bolibana.models.ScheduledReporting import ScheduledReporting
from bolibana.models.ExpectedReporting import ExpectedReporting
from bolibana.models.EntityType import EntityType
from bolibana.models.Period import Period
from bolibana.admin import EntityAdmin, EntityTypeAdmin, PeriodAdmin
from bolibana.models.Role import Role
from bolibana.models.Permission import Permission
from bolibana.models.Access import Access
from bolibana.models.Provider import Provider
from bolibana.admin import (RoleAdmin, PermissionAdmin,
                            AccessAdmin, ProviderAdmin)
from snisi_core.models.MalariaReport import MalariaR, AggMalariaR
from snisi_core.models.MaternalMortalityReport import (MaternalDeathR,
                                                       AggMaternalDeathR)
from snisi_core.models.CommoditiesReport import RHProductsR, AggRHProductsR
from snisi_core.models.ChildrenMortalityReport import (ChildrenDeathR,
                                                       AggChildrenDeathR)
from snisi_core.models.Epidemiology import EpidemiologyR
from snisi_core.models.BednetReport import BednetR
from snisi_core.models.alert import Alert
from snisi_core.admin import MalariaRAdmin, AlertAdmin

admin.site.register(Provider, ProviderAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(EntityType, EntityTypeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Access, AccessAdmin)
admin.site.register(Permission, PermissionAdmin)

admin.site.register(MalariaR, MalariaRAdmin)
admin.site.register(AggMalariaR)
admin.site.register(Alert, AlertAdmin)
admin.site.register(MaternalDeathR)
admin.site.register(AggMaternalDeathR)
admin.site.register(ChildrenDeathR)
admin.site.register(AggChildrenDeathR)
admin.site.register(RHProductsR)
admin.site.register(AggRHProductsR)
admin.site.register(EpidemiologyR)
admin.site.register(BednetR)
admin.site.register(ReportClass)
admin.site.register(ScheduledReporting)
admin.site.register(ExpectedReporting)