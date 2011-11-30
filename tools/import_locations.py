#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from bolibana.models import Entity, EntityType


def import_locations(csv_file, use_code=False):
    """ creates Entity object off a CSV filename

    CSV FORMAT:
    NAME, CODE, TYPE CODE (N,R,D,C), PARENT NAME, PARENT_ADDRESS
    CSV file must NOT include header row. """

    f = open(csv_file)
    for line in f.readlines():
        # explode CSV line
        name, code, type_code, \
        parent_name, parent_address = line.strip().split(',')

        # convert name to unicode for django & .title()
        try:
            name = unicode(name, 'utf-8')
        except:
            pass

        # retrieve parent object if address is provided
        try:
            if use_code:
                parent = Entity.objects.get(slug=parent_address)
            else:
                parent_id = int(parent_address[4:])
                parent = Entity.objects.get(id=parent_id)
        except ValueError:
            parent = None

        # retrieve type from code
        if type_code == 'N':
            type = EntityType.objects.get(slug='national')
        if type_code == 'R':
            type = EntityType.objects.get(slug='region')
        if type_code == 'D':
            type = EntityType.objects.get(slug='district')
        if type_code == 'C':
            type = EntityType.objects.get(slug='cscom')

        # create and save object
        entity = Entity(name=name.title(), type=type, \
                        slug=code.lower(), parent=parent)
        entity.save()

        print("%s: %s" % (entity.name, type))
    f.close()

if __name__ == '__main__':
    if sys.argv.__len__() < 2:
        print("No CSV file specified. exiting.")
        exit(1)

    import_locations(sys.argv[1])
