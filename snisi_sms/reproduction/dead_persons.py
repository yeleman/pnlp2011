#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import logging
import reversion
import locale

from django.conf import settings
from snisi_core.models.MaternalMortalityReport import MaternalMortalityReport
from snisi_core.models.ChildrenMortalityReport import ChildrenMortalityReport
from snisi_core.validators.reproduction import (ChildrenMortalityReportValidator, \
                                   MaternalMortalityReportValidator)
from bolibana.models import Entity
from snisi_sms.common import contact_for, parse_age_dob

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)
SEX = {
    'm': ChildrenMortalityReport.MALE,
    'f': ChildrenMortalityReport.FEMALE
}

DEATHPLACE = {
    'd': ChildrenMortalityReport.HOME,
    'c': ChildrenMortalityReport.CENTER,
    'a': ChildrenMortalityReport.OTHER,
}

DEATH_CAUSES_MAT = {
    'b': MaternalMortalityReport.CAUSE_BLEEDING,
    'f': MaternalMortalityReport.CAUSE_FEVER,
    'h': MaternalMortalityReport.CAUSE_HTN,
    'd': MaternalMortalityReport.CAUSE_DIARRHEA,
    'c': MaternalMortalityReport.CAUSE_CRISIS,
    'm': MaternalMortalityReport.CAUSE_MISCARRIAGE,
    'a': MaternalMortalityReport.CAUSE_ABORTION,
    'o': MaternalMortalityReport.CAUSE_OTHER,
}

DEATH_CAUSES_U5 = {
    'f': ChildrenMortalityReport.CAUSE_FEVER,
    'd': ChildrenMortalityReport.CAUSE_DIARRHEA,
    'b': ChildrenMortalityReport.CAUSE_DYSPNEA,
    'a': ChildrenMortalityReport.CAUSE_ANEMIA,
    'r': ChildrenMortalityReport.CAUSE_RASH,
    'c': ChildrenMortalityReport.CAUSE_COUGH,
    'v': ChildrenMortalityReport.CAUSE_VOMITING,
    'n': ChildrenMortalityReport.CAUSE_NUCHAL_RIGIDITY,
    'e': ChildrenMortalityReport.CAUSE_RED_EYE,
    't': ChildrenMortalityReport.CAUSE_EAT_REFUSAL,
    'o': ChildrenMortalityReport.CAUSE_OTHER,
}


class MaternalMortalityDataHolder(object):

    def get(self, slug):
        return getattr(self, slug)

    def field_name(self, slug):
        return ChildrenMortalityReport._meta.get_field(slug).verbose_name

    def set(self, slug, data):
        try:
            setattr(self, slug, data)
        except AttributeError:
            exec 'self.%s = None' % slug
            setattr(self, slug, data)

    def fields_for(self):
        fields = ['name', \
                    'dob', \
                    'dob_auto', \
                    'dod', \
                    'death_location', \
                    'living_children', \
                    'dead_children', \
                    'pregnant', \
                    'pregnancy_weeks', \
                    'pregnancy_related_death', \
                    'cause_of_death']

        return fields

    def data_for_cat(self, as_dict=False):
        data = []
        for field in self.fields_for():
            data.append(self.get(field))
        return data


def unfpa_dead_pregnant_woman(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap dpw profile reccord_date reporting_location_code
                      name age_or_dob dod_text death_location_code
                      living_children_text dead_children_text pregnant_text
                      pregnancy_weeks_text pregnancy_related_death_text
            exemple: 'fnuap dpw f 20120524 bana kona_diarra 20120524 20120524
                      bana 1 0 0 - 0 m'

         Outgoing:
            [SUCCES] Le rapport de deces name a ete enregistre.
            or [ERREUR] message """

    # common start of error message
    error_start = u"Impossible d'enregistrer le rapport. "
    try:
        args_names = ['profile',
        'reccord_date',
        'reporting_location',
        'name',
        'age_or_dob',
        'dod_text',
        'death_location',
        'living_children_text',
        'dead_children',
        'pregnant_text',
        'pregnancy_weeks_text',
        'pregnancy_related_death_text',
        'cause_of_death']
        args_values = args.split()
        arguments = dict(zip(args_names, args_values))
    except:
        message.respond(error_start + u" Le format du SMS est incorrect.")
        return True

    # convert form-data to int or bool respectively
    for key, value in arguments.items():
        if key == 'name':
            arguments[key] = value.replace('_', ' ')
        if key == 'cause_of_death':
            arguments[key] = DEATH_CAUSES_MAT.get(arguments[key],
                                     MaternalMortalityReport.CAUSE_OTHER)
        if key == 'pregnancy_weeks_text':
            try:
                arguments[key] = int(value)
            except:
                arguments[key] = 0

    # create a data holder for validator
    data_browser = MaternalMortalityDataHolder()

    # feed data holder with sms provided data
    for key, value in arguments.items():
        data_browser.set(key, value)
    provider = contact_for(message.identity)
    if not provider:
        message.respond(error_start + u"Aucun utilisateur ne possede ce " \
                                      u"numero de telephone")
        return True

    data_browser.set('reporting_location', arguments['reporting_location'])
    data_browser.set('death_location', arguments['death_location'])

    data_browser.set('author', provider.name())
    data_browser.set('pregnant', bool(int(arguments['pregnant_text'])))

    data_browser.set('pregnancy_weeks', \
                     int(arguments['pregnancy_weeks_text']))

    data_browser.set('pregnancy_related_death', \
                     bool(int(arguments['pregnancy_related_death_text'])))

    # create validator and fire
    validator = MaternalMortalityReportValidator(data_browser, author=provider)

    validator.errors.reset()
    try:
        validator.validate()
    except AttributeError as e:
        message.respond(error_start + e.__str__())
        return True

    errors = validator.errors
    # return first error to user
    if errors.count() > 0:
        message.respond(error_start + errors.all()[0])
        return True

    try:
        dob, dob_auto = parse_age_dob(arguments['age_or_dob'])
        dod = parse_age_dob(arguments['dod_text'], True)
        reporting_location = Entity.objects.get(slug=data_browser \
                                           .get('reporting_location'))
        death_location = Entity.objects.get(slug=data_browser \
                                           .get('death_location'))
        data_browser.set('dob', dob)
        data_browser.set('dob_auto', dob_auto)
        data_browser.set('dod', dod)
        data_browser.set('living_children', arguments['living_children_text'])
        report = MaternalMortalityReport.start(reporting_location, \
                                               death_location, provider)
        report.add_data(*data_browser.data_for_cat())
        with reversion.create_revision():
            report.save()
            reversion.set_user(provider.user)

    except Exception as e:
        message.respond(error_start + u"Une erreur technique s'est " \
                        u"produite. Reessayez plus tard et " \
                        u"contactez ANTIM si le probleme persiste.")
        logger.error(u"Unable to save report to DB. Message: %s | Exp: %r" \
                     % (message.content, e))
        return True
    message.respond(u"[SUCCES] Le rapport de deces de %(name)s a"
                    u" ete enregistre." % {'name': report.name})


class ChildrenMortalityDataHolder(object):

    def get(self, slug):
        return getattr(self, slug)

    def field_name(self, slug):
        return ChildrenMortalityReport._meta.get_field(slug).verbose_name

    def set(self, slug, data):
        try:
            setattr(self, slug, data)
        except AttributeError:
            exec 'self.%s = None' % slug
            setattr(self, slug, data)

    def fields_for(self):
        fields = ['name', \
                    'sex', \
                    'dob', \
                    'dob_auto', \
                    'dod', \
                    'death_place', \
                    'cause_of_death']

        return fields

    def data_for_cat(self, as_dict=False):
        data = []
        for field in self.fields_for():
            data.append(self.get(field))
        return data


def unfpa_dead_children_under5(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap du5 profile reccord_date reporting_location_code name sex
            age_or_dob dod_text death_location_code place_death
         exemple: 'fnuap du5 f 20120502 wolo nom F 20100502 20120502 wolo D o'

         Outgoing:
            [SUCCES] Le rapport de deces name a ete enregistre.
            or [ERREUR] message """

    # common start of error message
    error_start = u"Impossible d'enregistrer le rapport. "
    try:
        args_names = ['profile',
        'reccord_date',
        'reporting_location',
        'name',
        'sex',
        'age_or_dob',
        'dod_text',
        'death_location',
        'death_place',
        'cause_of_death']
        args_values = args.split()
        arguments = dict(zip(args_names, args_values))
    except:
        message.respond(error_start + u" Le format du SMS est incorrect.")
        return True
    # convert form-data to int or bool respectively
    for key, value in arguments.items():
        if key == 'name':
            arguments[key] = value.replace('_', ' ')
        if key == 'sex':
            arguments[key] = SEX.get(arguments[key],
                                     ChildrenMortalityReport.MALE)
        if key == 'place_death':
            arguments[key] = DEATHPLACE.get(arguments[key],
                                     ChildrenMortalityReport.OTHER)
        if key == 'cause_of_death_text':
            arguments[key] = DEATH_CAUSES_U5.get(arguments[key],
                                     ChildrenMortalityReport.CAUSE_OTHER)

    # create a data holder for validator
    data_browser = ChildrenMortalityDataHolder()

    # feed data holder with sms provided data
    for key, value in arguments.items():
        data_browser.set(key, value)

    provider = contact_for(message.identity)
    if not provider:
        message.respond(error_start + u"Aucun utilisateur ne possede ce " \
                                      u"numero de telephone")
        return True

    data_browser.set('reporting_location', arguments['reporting_location'])
    data_browser.set('death_location', arguments['death_location'])
    data_browser.set('author', provider.name())
    # create validator and fire
    validator = ChildrenMortalityReportValidator(data_browser, author=provider)

    validator.errors.reset()
    try:
        validator.validate()
    except AttributeError as e:
        message.respond(error_start + e.__str__())
        return True
    errors = validator.errors
    # return first error to user
    if errors.count() > 0:
        message.respond(error_start + errors.all()[0])
        return True
    try:
        dob, dob_auto = parse_age_dob(arguments['age_or_dob'])
        dod = parse_age_dob(arguments['dod_text'], True)
        reporting_location = Entity.objects.get(slug=data_browser \
                                           .get('reporting_location'))
        death_location = Entity.objects.get(slug=data_browser \
                                           .get('death_location'))
        data_browser.set('dob', dob)
        data_browser.set('dob_auto', dob_auto)
        data_browser.set('dod', dod)
        report = ChildrenMortalityReport.start(reporting_location, \
                                               death_location, provider)

        report.add_data(*data_browser.data_for_cat())
        with reversion.create_revision():
            report.save()
            reversion.set_user(provider.user)

    except Exception as e:
        message.respond(error_start + u"Une erreur technique s'est " \
                        u"produite. Reessayez plus tard et " \
                        u"contactez ANTIM si le probleme persiste.")
        logger.error(u"Unable to save report to DB. Message: %s | Exp: %r" \
                     % (message.content, e))
        return True

    message.respond(u"[SUCCES] Le rapport de deces de %(name)s a"
                    u" ete enregistre." % {'name': report.name})
