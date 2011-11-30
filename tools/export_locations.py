#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from bolibana.models import Entity, EntityType

def type_code(entity):
    c = entity.type.slug
    return c[0].upper()

def export_locations(csv_file, compat_import=False):
    """ Export Entity objects into a CSV file

    CSV FORMAT:
    REGION, DISTRICT, CSCOM, CODE, TYPE

    NAME, CODE, TYPE CODE (N,R,D,C), PARENT NAME, PARENT_ADDRESS
    """

    errors = []

    #def region_for(e):
    def get_ancestors(entity, include_self=True):
        ancestors = []
        ee = entity if include_self else entity.parent
        while ee.parent:
            ancestors.append(ee)
            ee = ee.parent
        ancestors.append(ee)
        ancestors.reverse()
        return ancestors

    first = True
    f = open(csv_file, 'w')

    if not compat_import:
        header = u"Région,District,Unité sanitaire,Code,Niveau\n"
        f.write(header.encode('utf-8'))

    for entity in Entity.objects.all().order_by('parent'):

        if not entity.parent:
            continue

        #anc = u",".join([e.display_name() for e in entity.get_ancestors(include_self=True)[1:]])
        anc = u",".join([e.display_name() for e in get_ancestors(entity, include_self=True)[1:]])



        if entity.type.slug == 'district':
            anc += ','
        if entity.type.slug == 'region':
            anc += ',,'
        line = u"%(anc)s,%(code)s,%(type)s\n" % {'anc': anc, 'code': entity.slug, 'type': entity.type}

        if compat_import:

            line = "%(nam)s,%(cod)s,%(typ)s,%(par)s,%(parcode)s" % {'nam': entity.name.title(), 'cod': entity.slug, 'typ': type_code(entity), 'par': entity.parent.name.title(), 'parcode': entity.parent.slug}

        f.write(line.encode('utf-8'))
        print(entity)
    f.close()

if __name__ == '__main__':
    if sys.argv.__len__() < 2:
        print("No CSV file specified. exiting.")
        exit(1)

    export_locations(sys.argv[1])
