#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from bolibana.models.Role import Role
from bolibana.models.Provider import Provider
from bolibana.models.Access import Access
from bolibana.auth.utils import username_from_name, random_password
from bolibana.models import Entity


def import_users(csv_file):
    """ creates Provider object off a CSV filename

    CSV FORMAT:
    FIRST NAME, LAST NAME, EMAIL, PHONE, PHONE2, ROLE CODE, ENTITY CODE
    CSV file MUST include header row. """

    errors = []

    first = True
    f = open(csv_file)
    succ = open('success.csv', 'w')
    for line in f.readlines():
        if first:
            first = False
            continue
        # explode CSV line
        fname, lname, email, \
        phone_number, phone2, role_code, entity_code, area = line.strip().split(',')

        # convert name to unicode for django & .title()
        try:
            fname = unicode(fname.strip(), 'utf-8').title()
        except:
            pass

        try:
            lname = unicode(lname.strip(), 'utf-8').title()
        except:
            pass

        # retrieve parent object if address is provided
        try:
            entity = Entity.objects.get(slug=entity_code.lower())
        except:
            print("BAD ENTITY: %s" % entity_code)
            #raise
            errors.append(line)
            continue

        try:
            role = Role.objects.get(slug=role_code.lower())
        except:
            print("BAD ROLE: %s" % role_code)
            #raise
            errors.append(line)
            continue

        # build an Access based on Role and Entity selected
        # if a national role, force attachment to root entity
        if role.slug in ('antim', 'national'):
            entity = Entity.objects.filter(level=0)[0]
        elif role.slug != entity.type.slug:
            print("ROLE MISMATCH LOCATION TYPE: %s / %s (%s)" % (role_code, entity_code, entity.type))
            errors.append(line)
            continue
        access = Access.find_by(role, entity)

        # forge username
        username = username_from_name(fname, lname)
        # generate password
        password = random_password()

        pcount = Provider.objects.filter(phone_number=phone_number).count()

        if phone_number and pcount > 0:
            print("PHONE NUMBER CONFLICT: %s" % phone_number)
            errors.append(line)
            continue

        # create Provider
        provider = Provider.create_provider(username, \
                                            'xx', access=[access])
        provider.set_password(password)

        # we have a valid provider whatever the case. update details
        provider.first_name = fname
        provider.last_name = lname
        provider.email = email
        # only update if not None to preserve uniqueness

        if phone_number and pcount == 0:
            provider.phone_number = phone_number

        if phone2:
            provider.phone_number_extra = phone2

        provider.save()

        line = u"%(ent)s,%(role)s,%(fname)s,%(lname)s,%(user)s,%(pass)s,%(passenc)s\n" % {'ent': entity, 'role': role, 'fname': provider.first_name, 'lname': provider.last_name, 'user': username, 'pass': password, 'passenc': provider.user.password}
        succ.write(line.encode('utf-8'))
        print(provider.name_access())
    f.close()
    succ.close()

    if errors:
        error_file = 'errors.csv'
        f = open(error_file, 'w')
        for line in errors:
            f.write(line)
        f.close()
        print("%d errors appended to file %s" % (errors.__len__(), error_file))

if __name__ == '__main__':
    if sys.argv.__len__() < 2:
        print("No CSV file specified. exiting.")
        exit(1)

    import_users(sys.argv[1])
