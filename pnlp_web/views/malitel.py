#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

from pnlp_core.data import contact_for
from bolibana.models import Entity

from django.db.models.query import Q
from django.shortcuts import render

def malitel_list(request):
    context = {'category': 'malitel'}
    entities = Entity.objects.filter(Q(parent__slug='maci') | Q(parent__slug='nion'))
    for entity in entities:
        entity.contact = contact_for(entity).phone_number
    context.update({'entities': entities})

    return render(request, 'malitel.html', context)
