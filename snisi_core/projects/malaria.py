#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

MALARIA_SLUG = 'malaria'
MALARIA_NAME = u"Malaria"

from bolibana.models.Project import Project


def get_malaria_project():
    try:
        return Project.objects.get(slug=MALARIA_SLUG)
    except Project.DoesNotExist:
        return Project.objects.create(slug=MALARIA_SLUG,
                                      name=MALARIA_NAME)
