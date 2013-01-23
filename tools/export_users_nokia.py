#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from bolibana.models.Provider import Provider


def filter_pilot_cscom(provider):
    """ return True if provider is part of pilot CSCOM """

    return provider.first_role().slug == 'cscom' \
       and provider.first_target().parent.slug in ('nion', 'maci')


def filter_none(provider):
    return True


def filter_district(provider):
    """ return True if district role """

    return provider.first_role().slug == 'district'


def filter_region(provider):
    """ return True if district role """

    return provider.first_role().slug == 'region'


def filter_district_region(provider):
    return filter_district(provider) or filter_region(provider)


def export_users(csv_file, provider_filter=filter_none):

    count = 0

    f = open(csv_file, 'w')

    header = u'"Title";"First name";"Middle name";"Last name";"Suffix";"Job title";"Company";"Birthday";"SIP address";"Push-to-talk";"Share view";"User ID";"Notes";"General mobile";"General phone";"General e-mail";"General fax";"General video call";"General web address";"General VOIP address";"General P.O.Box";"General extension";"General street";"General postal/ZIP code";"General city";"General state/province";"General country/region";"Home mobile";"Home phone";"Home e-mail";"Home fax";"Home video call";"Home web address";"Home VOIP address";"Home P.O.Box";"Home extension";"Home street";"Home postal/ZIP code";"Home city";"Home state/province";"Home country/region";"Business mobile";"Business phone";"Business e-mail";"Business fax";"Business video call";"Business web address";"Business VOIP address";"Business P.O.Box";"Business extension";"Business street";"Business postal/ZIP code";"Business city";"Business state/province";"Business country/region";""\n'

    f.write(header)

    for provider in Provider.objects.all():

        if not provider_filter.__call__(provider):
            continue

        count += 1

        tpl = u'"";"%(fname)s";"";"%(lname)s";"";"%(role)s";"%(target)s";"";"";"";"";"";"";"%(phone)s";"%(phone2)s";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";""\n'

        line = tpl % {'fname': provider.first_name,
                      'lname': provider.last_name,
                      'role': provider.first_role(),
                      'target': provider.first_target(),
                      'phone': provider.phone_number,
                      'phone2': provider.phone_number_extra}

        print(u"%(prov)s %(phone)s" % {'phone': provider.phone_number,
                                       'prov': provider})

        try:
            f.write(line.encode('ISO-8859-15'))
        except Exception as e:
            print(u"Error: %s - %s" % (provider, e))

    f.close()
    print(count)
