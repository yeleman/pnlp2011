#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import date

from django.utils.translation import ugettext as _
from bolibana.reporting.validator import DataValidator
from bolibana.models.Entity import Entity
from bolibana.models.Period import MonthPeriod
from snisi_core.models.CommoditiesReport import RHProductsR
from snisi_sms.common import parse_age_dob, date_is_old


class RHCommoditiesReportValidator(DataValidator):

    """ Monthly RHCommodities Routine Report from CSCOM data validation """

    def validate(self):
        """ Test whether attached data matches PNLP's logic requirements """

        from snisi_core.data import (provider_can, time_cscom_over,
                            time_district_over, time_region_over)

        # PERIOD MONTH
        # range(1, 12)
        # already handled.

        # PERIOD YEAR
        # range(2010, 2020)
        # already handled

        # NO FUTURE
        year = int(self.get('reporting_year'))
        month = int(self.get('reporting_month'))
        if year >= date.today().year \
           and self.get('reporting_month') >= date.today().month:
            self.errors.add(_(u"The period of data (%(period)s) "
                            "is in the future.") %
                            {'period': u"%s %d" %
                                       (month.__str__().zfill(2),
                                        year)}, 'period')

        # NO PAST
        period = MonthPeriod.find_create_from(year=year, month=month)

        if self.options.is_editing:
            if self.options.level == 'district':
                time_over = time_district_over
            elif self.options.level == 'region':
                time_over = time_region_over
            else:
                time_over = time_cscom_over
        else:
            time_over = time_cscom_over

        if time_over(period) and not self.options.bulk_import:
            self.errors.add(_(u"The reporting time frame for that "
                              "period (%(period)s) is over.")
                            % {'period': period}, 'period')

        # date DAY / MONTH / YEAR
        try:
            date(self.get('fillin_year'),
                 self.get('fillin_month'), self.get('fillin_day'))
        except ValueError:
            self.errors.add(_(u"The fillin day (%(day)s) is out of range "
                            "for that month (%(month)s)") \
                            % {'day':
                                   self.get('fillin_day').__str__().zfill(2),
                               'month':
                                self.get('fillin_month').__str__().zfill(2)},
                               'fillin')

        # ENTITY
        try:
            entity = Entity.objects.get(slug=self.get('entity'),
                                        type__slug='cscom')
        except Entity.DoesNotExist:
            entity = None
            self.errors.add(_(u"The entity code (%(code)s) does not "
                              "match any HC.") % {'code':
                                                  self.get('entity')}, 'period')

        # NO DUPLICATE
        if not self.options.data_only:
            period = MonthPeriod.find_create_from(year=year,
                                                  month=month)
            if entity \
            and RHProductsR.objects.filter(entity=entity,
                                           period=period).count() > 0:
                report = RHProductsR.objects.get(entity=entity, \
                                                         period=period)
                self.errors.add(_(u"There is already a report for "
                                  "that HC (%(entity)s) and that "
                                  "period (%(period)s)") %
                                  {'entity': entity.display_full_name(),
                                   'period': period.name()}
                                   + u" Recu: %s." % report.receipt, 'period')

        # User can create such report
        if self.options.author:
            if not provider_can('can_submit_report',
                                self.options.author, entity) \
               and not self.options.bulk_import:
                self.errors.add(_(u"You don't have permission to send " \
                                  "a report for that "
                                  "location (%(loc)s).")
                                % {'loc': entity.display_full_name()})


class ChildrenMortalityReportValidator(DataValidator):
    """ """

    def validate(self):
        """ """

        # reporting location
        try:
            Entity.objects.get(slug=self.get('reporting_location'))
        except Entity.DoesNotExist:
            self.errors.add(_(u"The entity code (%(code)s) does not "
                              "match any HC.") % {'code':
                                                  self.get('reporting_location')},
                                                  'period')

        # DOB (YYYY-MM-DD) or age (11a/11m)
        try:
            dob, dob_auto = parse_age_dob(str(self.get('age_or_dob')))
        except:
            self.errors.add(_(u"[ERREUR] la date de naissance n'est pas valide."))

        # reccord date
        try:
            reccord_date, _reccord_date = parse_age_dob(self.get('reccord_date'))
        except:
            self.errors.add(_(u"[Date de visite] la date n'est pas valide."))

        try:
            date_is_old(reccord_date)
        except ValueError, e:
            self.errors.add(_(u"[ERREUR] %s" % e))

        # Date of Death, YYYY-MM-DD
        try:
            parse_age_dob(self.get('dod_text'), True)
        except:
            self.errors.add(_(u"[ERREUR] la date de décès n'est pas valide"))

        # Place of death, entity code
        try:
            entity = Entity.objects.get(slug=self.get('death_location'))
        except Entity.DoesNotExist:
            self.errors.add(_(u"The entity code (%(code)s) does not "
                              "match any HC.") % {'code': \
                                                  self.get('death_location')},
                                                  'period')

        # User can create such report
        if self.options.author:
            if not provider_can('can_submit_report',
                                self.options.author, entity) \
               and not self.options.bulk_import:
                self.errors.add(_(u"You don't have permission to send "
                                  "a report for that "
                                  "location (%(loc)s).")
                                % {'loc': entity.display_full_name()})


class MaternalMortalityReportValidator(DataValidator):
    """ """

    def validate(self):
        """ """
        from snisi_core.data import provider_can
        # reporting location
        try:
            Entity.objects.get(slug=self.get('reporting_location'))
        except Entity.DoesNotExist:
            self.errors.add(_(u"The entity code (%(code)s) does not "
                              "match any HC.") % {'code':
                                                  self.get('reporting_location')},
                                                  'period')

        # DOB (YYYY-MM-DD) or age (11a/11m)
        try:
            dob, dob_auto = parse_age_dob(str(self.get('age_or_dob')))
        except:
            self.errors.add(_(u"[ERREUR] la date de naissance n'est pas valide."))

        # reccord date
        try:
            reccord_date, _reccord_date = parse_age_dob(self.get('reccord_date'))
        except:
            self.errors.add(_(u"[Date de visite] la date n'est pas valide."))

        try:
            date_is_old(reccord_date)
        except ValueError, e:
            self.errors.add(_(u"[ERREUR] %s" % e))

        # Nb of living children
        try:
            int(self.get('living_children_text'))
        except:
            self.errors.add(_(u"le nombre d'enfants vivant du defunt"))

        # Nb of dead children
        try:
            int(self.get('dead_children'))
        except:
            self.errors.add(_(u"le nombre d'enfants morts de la"
                                   u" personne decedee"))

        # Date of Death, YYYY-MM-DD
        try:
            parse_age_dob(self.get('dod_text'), True)
        except:
            self.errors.add(_(u"[ERREUR] la date de décès n'est pas valide"))

        # Place of death, entity code
        try:
            entity = Entity.objects.get(slug=self.get('death_location'))
        except Entity.DoesNotExist:
            self.errors.add(_(u"The entity code (%(code)s) does not "
                              "match any HC.") % {'code':
                                                  self.get('death_location')},
                                                  'period')

        # User can create such report
        if self.options.author:
            if not provider_can('can_submit_report',
                                self.options.author, entity) \
               and not self.options.bulk_import:
                self.errors.add(_(u"You don't have permission to send "
                                  "a report for that "
                                  "location (%(loc)s).")
                                % {'loc': entity.display_full_name()})
