#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

from pnlp_core.data import contact_for
from bolibana.models import Entity

from django.db.models.query import Q
from django.shortcuts import render

def malitel_list(request):
    context = {'category': 'malitel'}
    entities = []
    for entity in Entity.objects.filter(Q(parent__slug='maci') | Q(parent__slug='nion')):
        pn = contact_for(entity).phone_number
        if '624175' in pn:
            entities.append({'name': entity, 'contact': pn})
    entities.sort(key=lambda x: x['contact'])
    context.update({'entities': entities})

    return render(request, 'malitel.html', context)
