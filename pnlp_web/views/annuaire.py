#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from django.shortcuts import render
from django.utils.translation import ugettext as _, ugettext_lazy
from django import forms
from mptt.fields import TreeNodeChoiceField

from pnlp_core.data import contact_for
from bolibana_auth.models import Role, Provider
from bolibana_reporting.models import Entity

class annuaireForm(forms.Form):

    role = forms.ChoiceField(label=ugettext_lazy(u"Role"), \
                             choices=[(role.slug, role.name) \
                                      for role \
                                      in Role.objects.all().order_by('name')])

    entity = TreeNodeChoiceField(queryset=Entity.tree.all(), \
                                 level_indicator=u'---', \
                                 label=ugettext_lazy(u"Entity"))


def annuaire_cscom(request, entity_id=None):

    form = annuaireForm()
    context = {'form':form}
    if request.method == "POST":
        form = annuaireForm(request.POST)
        name_role = request.POST["role"]
        entity_id = request.POST["entity"]

        contact_entity = [(ent, contact_for(ent)) \
                for ent in Entity.objects.filter(id=entity_id)]
        print contact_entity
        context.update({ 'contact_entity': contact_entity})

    return render(request, 'annuaire.html', context)
