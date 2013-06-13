#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django import forms

from snisi_core.models.ChildrenMortalityReport import (ChildrenDeathR,
                                                       AggChildrenDeathR)
from snisi_core.models.MaternalMortalityReport import (MaternalDeathR,
                                                       AggMaternalDeathR)
from snisi_core.models.CommoditiesReport import RHProductsR, AggRHProductsR
from snisi_core.data import COMMON_EXCLUDED_FIELDS


class ChildrenDeathRForm(forms.ModelForm):
    class Meta:
        model = ChildrenDeathR
        exclude = COMMON_EXCLUDED_FIELDS


class AggChildrenDeathRForm(forms.ModelForm):
    class Meta:
        model = AggChildrenDeathR
        exclude = COMMON_EXCLUDED_FIELDS


class MaternalDeathRForm(forms.ModelForm):
    class Meta:
        model = MaternalDeathR
        exclude = COMMON_EXCLUDED_FIELDS


class AggMaternalDeathRForm(forms.ModelForm):
    class Meta:
        model = AggMaternalDeathR
        exclude = COMMON_EXCLUDED_FIELDS


class RHProductsRForm(forms.ModelForm):
    class Meta:
        model = RHProductsR
        exclude = COMMON_EXCLUDED_FIELDS


class AggRHProductsRForm(forms.ModelForm):
    class Meta:
        model = AggRHProductsR
        exclude = COMMON_EXCLUDED_FIELDS
