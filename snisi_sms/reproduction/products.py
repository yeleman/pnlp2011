#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import datetime
import logging
import reversion

from snisi_core.models.CommoditiesReport import RHProductsR
from bolibana.models.Entity import Entity
from bolibana.models.Period import MonthPeriod
from snisi_core.validators.reproduction import RHProductsRValidator
from snisi_sms.common import contact_for


YESNOAVAIL = {
    '0': RHProductsR.SUPPLIES_NOT_PROVIDED,
    '1': RHProductsR.SUPPLIES_AVAILABLE,
    '2': RHProductsR.SUPPLIES_NOT_AVAILABLE,
}

logger = logging.getLogger(__name__)


class RHCommoditiesDataHolder(object):

    def get(self, slug):
        return getattr(self, slug)

    def field_name(self, slug):
        return RHProductsR._meta.get_field(slug).verbose_name

    def set(self, slug, data):
        try:
            setattr(self, slug, data)
        except AttributeError:
            exec 'self.%s = None' % slug
            setattr(self, slug, data)

    def fields_for(self):
        fields = ['family_planning',
                  'delivery_services',
                  'male_condom',
                  'female_condom',
                  'oral_pills',
                  'injectable',
                  'iud',
                  'implants',
                  'female_sterilization',
                  'male_sterilization',
                  'amoxicillin_ij',
                  'amoxicillin_cap_gel',
                  'amoxicillin_suspension',
                  'azithromycine_tab',
                  'azithromycine_suspension',
                  'benzathine_penicillin',
                  'cefexime',
                  'clotrimazole',
                  'ergometrine_tab',
                  'ergometrine_vials',
                  'iron',
                  'folate',
                  'iron_folate',
                  'magnesium_sulfate',
                  'metronidazole',
                  'oxytocine',
                  'ceftriaxone_500',
                  'ceftriaxone_1000']

        return fields

    def data_for_cat(self, as_dict=False):
        data = []
        for field in self.fields_for():
            data.append(self.get(field))
        return data


def unfpa_monthly_product_stockouts(message, args, sub_cmd, **kwargs):
    """  Incomming:
            fnuap mps year month family_planning delivery_services male_condom
            female_condom oral_pills injectable iud implants
            female_sterilization male_sterilization
            amoxicillin_ij amoxicillin_cap_gel
            amoxicillin_suspension azithromycine_tab
            azithromycine_suspension benzathine_penicillin cefexime
            clotrimazole ergometrine_tab ergometrine_vials iron
            folate iron_folate magnesium_sulfate metronidazole
            oxytocine ceftriaxone_500 ceftriaxone_1000 comment
        example:
           'fnuap mps 2012 05 wolo 0 0 20 - - - - - 0 0 - - - - - - - - - - - -
             - - - - - - -'
        Outgoing:
            [SUCCES] Le rapport de name a ete enregistre.
            or [ERREUR] message """

    # common start of error message
    error_start = u"Impossible d'enregistrer le rapport. "

    try:
        # -1 represente le non disponible
        args = args.replace("-", "-1")
        args_names = ['reporting_year',
        'reporting_month',
        'location_of_sdp',
        'family_planning',
        'delivery_services',
        'male_condom',
        'female_condom',
        'oral_pills',
        'injectable',
        'iud',
        'implants',
        'female_sterilization',
        'male_sterilization',
        'amoxicillin_ij',
        'amoxicillin_cap_gel',
        'amoxicillin_suspension',
        'azithromycine_tab',
        'azithromycine_suspension',
        'benzathine_penicillin',
        'cefexime',
        'clotrimazole',
        'ergometrine_tab',
        'ergometrine_vials',
        'iron',
        'folate',
        'iron_folate',
        'magnesium_sulfate',
        'metronidazole',
        'oxytocine',
        'ceftriaxone_500',
        'ceftriaxone_1000',
        'comment']
        args_values = args.split()
        arguments = dict(zip(args_names, args_values))
    except:
        message.respond(error_start + u" Le format du SMS est incorrect.")
        return True

    def check_int(val):
        try:
            return int(val)
        except:
            return -1

    # convert form-data to int or bool respectively
    for key, value in arguments.items():
        if not key in ['location_of_sdp', 'location_of_sdp', 'reporting_year',
                       'reporting_month']:
            arguments[key] = check_int(value)

    try:
        arguments['comment'] = arguments['comment'].replace(u"_", u" ")
    except:
        arguments['comment'] = u""

    provider = contact_for(message.identity)
    if not provider:
        message.respond(error_start + u"Aucun utilisateur ne possede ce "
                                      u"numero de telephone")
        return True

    # now we have well formed and authenticated data.
    # let's check for business-logic errors.

    # create a data holder for validator
    data_browser = RHCommoditiesDataHolder()

    # feed data holder with sms provided data
    for key, value in arguments.items():
        data_browser.set(key, value)

    data_browser.set('entity', arguments['location_of_sdp'])
    today = datetime.date.today()
    data_browser.set('fillin_day', today.day)
    data_browser.set('fillin_month', today.month)
    data_browser.set('fillin_year', today.year)
    data_browser.set('author', provider.name())

    # create validator and fire
    validator = RHProductsRValidator(data_browser, author=provider)

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

    from snisi_core.data import time_is_prompt

    try:
        period = MonthPeriod.find_create_from(year=int(data_browser
                                            .get('reporting_year')),
                                              month=int(data_browser
                                            .get('reporting_month')))
        is_late = not time_is_prompt(period)
        entity = Entity.objects.get(slug=data_browser.get('location_of_sdp'),
                                    type__slug='cscom')
        # create the report
        report = RHProductsR.start(period, entity, provider,
                                   type=RHProductsR.TYPE_SOURCE,
                                   is_late=is_late)

        report.add_data(*data_browser.data_for_cat())
        with reversion.create_revision():
            report.save()
            reversion.set_user(provider.user)
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
