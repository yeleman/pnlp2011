#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import datetime
import logging
import reversion
import locale

from django.conf import settings

from snisi_core.models.Epidemiology import EpidemiologyR
from snisi_core.validators.epidemiology import EpidemiologyReportValidator
from bolibana.models.Entity import Entity
from bolibana.models.Period import WeekPeriod
from snisi_sms.common import contact_for

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


class EpidemiologyDataHolder(object):

    def get(self, slug):
        return getattr(self, slug)

    def field_name(self, slug):
        return EpidemiologyR._meta.get_field(slug).verbose_name

    def set(self, slug, data):
        try:
            setattr(self, slug, data)
        except AttributeError:
            exec 'self.%s = None' % slug
            setattr(self, slug, data)

    def fields_for(self):
        fields = ['acute_flaccid_paralysis_case',
                  'acute_flaccid_paralysis_death',
                  'influenza_a_h1n1_case',
                  'influenza_a_h1n1_death',
                  'cholera_case',
                  'cholera_death',
                  'red_diarrhea_case',
                  'red_diarrhea_death',
                  'measles_case',
                  'measles_death',
                  'yellow_fever_case',
                  'yellow_fever_death',
                  'neonatal_tetanus_case',
                  'neonatal_tetanus_death',
                  'meningitis_case',
                  'meningitis_death',
                  'rabies_case',
                  'rabies_death',
                  'acute_measles_diarrhea_case',
                  'acute_measles_diarrhea_death',
                  'other_notifiable_disease_case',
                  'other_notifiable_disease_death']

        return fields

    def data_for_cat(self, as_dict=False):
        data = []
        for field in self.fields_for():
            data.append(self.get(field))
        return data


def epidemiology_handler(message):
    def main_epidemiology_handler(message):
        if message.content.lower().startswith('epid '):
            if message.content.lower().startswith('epid passwd'):
                pass
            elif message.content.lower().strip() == 'epid aide':
                pass
            elif message.content.lower().startswith('epid aide'):
                pass
            else:
                return epidemiology(message)
        else:
            return False

    if main_epidemiology_handler(message):
        message.status = message.STATUS_PROCESSED
        message.save()
        logger.info(u"[HANDLED] msg: %s" % message)
        return True
    logger.info(u"[NOT HANDLED] msg : %s" % message)
    return False


def epidemiology(message, **kwargs):
    """  Incomming:
             epid year number_week code_reporting_location

        example:
           'epid 2012 1 v01619 1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8 9 9 10 10 11 11'

        Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    # common start of error message
    error_start = u"Impossible d'enregistrer le rapport. "

    try:
        args_names = ['kw1', 'reporting_year',
                      'reporting_week',
                      'location',
                      'acute_flaccid_paralysis_case',
                      'acute_flaccid_paralysis_death',
                      'influenza_a_h1n1_case',
                      'influenza_a_h1n1_death',
                      'cholera_case',
                      'cholera_death',
                      'red_diarrhea_case',
                      'red_diarrhea_death',
                      'measles_case',
                      'measles_death',
                      'yellow_fever_case',
                      'yellow_fever_death',
                      'neonatal_tetanus_case',
                      'neonatal_tetanus_death',
                      'meningitis_case',
                      'meningitis_death',
                      'rabies_case',
                      'rabies_death',
                      'acute_measles_diarrhea_case',
                      'acute_measles_diarrhea_death',
                      'other_notifiable_disease_case',
                      'other_notifiable_disease_death']
        args_values = message.content.strip().lower().split()
        arguments = dict(zip(args_names, args_values))
    except:
        message.respond(error_start + u" Le format du SMS est incorrect.")
        return True

    # convert form-data to int or bool respectively
    for key, value in arguments.items():
        if not key in ['location', 'kw1']:
            arguments[key] = int(value)

    provider = contact_for(message.identity)
    if not provider:
        message.respond(u"%s Aucun utilisateur ne possede ce "
                        u"numero de telephone" % error_start)
        return True

    # now we have well formed and authenticated data.
    # let's check for business-logic errors.

    # create a data holder for validator
    data_browser = EpidemiologyDataHolder()

    # feed data holder with sms provided data
    for key, value in arguments.items():
        data_browser.set(key, value)

    data_browser.set('entity', arguments['location'])
    today = datetime.date.today()
    data_browser.set('fillin_day', today.day)
    data_browser.set('fillin_month', today.month)
    data_browser.set('fillin_year', today.year)
    data_browser.set('author', provider.name())

    # create validator and fire
    validator = EpidemiologyReportValidator(data_browser, author=provider)

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
        period = WeekPeriod.find_create_by_weeknum(data_browser.get('reporting_year'),
                                                   data_browser.get('reporting_week'))
        # is_late = not time_is_prompt(period)
        entity = Entity.objects.get(slug=data_browser.get('location'),
                                    type__slug='cscom')
        # create the report
        report = EpidemiologyR.start(period, entity, provider,
                                     type=EpidemiologyR.TYPE_SOURCE)

        report.add_data(*data_browser.data_for_cat())
        with reversion.create_revision():
            report.save()
            reversion.set_user(provider)
    except Exception as e:
        message.respond(error_start + u"Une erreur technique s'est "
                        u"produite. Reessayez plus tard et "
                        u"contactez ANTIM si le probleme persiste.")
        logger.error(u"Unable to save report to DB. Message: %s | Exp: %r"
                     % (message.content, e))
        return True

    message.respond(u"[SUCCES] Le rapport de %(cscom)s pour %(period)s "
                    u"a ete enregistre. "
                    u"Le No de recu est #%(receipt)s."
                    % {'cscom': report.entity.display_full_name(),
                       'period': report.period,
                       'receipt': report.receipt})

    return True
