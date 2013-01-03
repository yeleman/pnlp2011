#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import date

from django.utils.translation import ugettext as _
from bolibana.reporting.validator import DataValidator
from bolibana.reporting.errors import MissingData
from bolibana.models import Entity, MonthPeriod, WeekPeriod
from snisi_core.models import (MalariaReport, RHCommoditiesReport,
                               EpidemiologyReport)
from snisi_core.data import (provider_can, time_cscom_over,
                            time_district_over, time_region_over)


class MalariaReportValidator(DataValidator):

    """ Monthly Malaria Routine Report from CSCOM data validation """

    def validate(self):
        """ Test whether attached data matches PNLP's logic requirements """

        no_more_than_text = _("%(field2)s (%(f2value)d) can't be more " \
                            "than %(field1)s (%(f1value)d)")
        allcats = ('u5', 'o5', 'pw')
        nopwcat = ('u5', 'o5')

        def test_value_under(fieldref, fieldtest, cats):
            for cat in cats:
                try:
                    dic = {'field2': self.field_name('%s_%s' \
                                                     % (cat, fieldtest)), \
                           'f2value': self.get('%s_%s' % (cat, fieldtest)), \
                           'field1': self.field_name('%s_%s' \
                                                     % (cat, fieldref)), \
                           'f1value': self.get('%s_%s' % (cat, fieldref))}
                    if dic['f1value'] < dic['f2value']:
                        self.errors.add(no_more_than_text % dic, cat)
                except MissingData:
                    # this missing data should have already been reported
                    pass

        # total > malaria cases
        test_value_under('total_consultation_all_causes', \
                         'total_suspected_malaria_cases', allcats)

        # total >  malaria simple
        test_value_under('total_consultation_all_causes', \
                         'total_simple_malaria_cases', nopwcat)

        # total >  malaria severe
        test_value_under('total_consultation_all_causes', \
                         'total_severe_malaria_cases', allcats)

        # suspected > malaria simple
        test_value_under('total_suspected_malaria_cases', \
                         'total_simple_malaria_cases', nopwcat)

        # suspected > malaria severe
        test_value_under('total_suspected_malaria_cases', \
                         'total_severe_malaria_cases', allcats)

        # suspected > malaria tested
        test_value_under('total_suspected_malaria_cases', \
                         'total_tested_malaria_cases', allcats)

        # suspected > malaria confirmed
        test_value_under('total_suspected_malaria_cases', \
                         'total_confirmed_malaria_cases', allcats)

        # suspected > simple + severe
        for cat in nopwcat:
            try:
                dic = {'field2': _(u"%(simple)s + %(severe)s") % {'simple': \
                      self.field_name('%s_total_simple_malaria_cases' % cat), \
                      'severe': \
                     self.field_name('%s_total_severe_malaria_cases' % cat)}, \
                      'f2value': int(self.get('%s_total_simple_malaria_cases' \
                                              % cat)) \
                               + int(self.get('%s_total_severe_malaria_cases' \
                                              % cat)), \
                      'field1': \
                           self.field_name('%s_total_suspected_malaria_cases' \
                                           % cat), \
                      'f1value': self.get('%s_total_suspected_malaria_cases' \
                                           % cat)}
                if dic['f1value'] < dic['f2value']:
                    self.errors.add(no_more_than_text % dic, cat)
            except MissingData:
                pass

        # confirmed > simple + severe
        for cat in nopwcat:
            try:
                dic = {'field2': _(u"%(simple)s + %(severe)s") % {'simple': \
                      self.field_name('%s_total_simple_malaria_cases' % cat), \
                      'severe': \
                     self.field_name('%s_total_severe_malaria_cases' % cat)}, \
                      'f2value': int(self.get('%s_total_simple_malaria_cases' \
                                              % cat)) \
                               + int(self.get('%s_total_severe_malaria_cases' \
                                              % cat)), \
                      'field1': \
                           self.field_name('%s_total_confirmed_malaria_cases' \
                                           % cat), \
                      'f1value': self.get('%s_total_confirmed_malaria_cases' \
                                           % cat)}
                if dic['f1value'] < dic['f2value']:
                    self.errors.add(no_more_than_text % dic, cat)
            except MissingData:
                pass

        # tested > confirmed
        test_value_under('total_tested_malaria_cases', \
                         'total_confirmed_malaria_cases', allcats)

        # tested > ACT
        test_value_under('total_tested_malaria_cases', \
                         'total_treated_malaria_cases', allcats)

        # confirmed > act
        test_value_under('total_confirmed_malaria_cases', \
                         'total_treated_malaria_cases', allcats)

        # total inpatient > malaria inpatient
        test_value_under('total_inpatient_all_causes', \
                         'total_malaria_inpatient', allcats)

        # total death > malaria death
        test_value_under('total_death_all_causes', \
                         'total_malaria_death', allcats)

        # PERIOD MONTH
        # range(1, 12)
        # already handled.

        # PERIOD YEAR
        # range(2010, 2020)
        # already handled

        # NO FUTURE
        if self.get('year') >= date.today().year \
           and self.get('month') >= date.today().month:
            self.errors.add(_(u"The period of data (%(period)s) " \
                            "is in the future.") % \
                            {'period': u"%s %d" % \
                                       (self.get('month').__str__().zfill(2), \
                                        self.get('year'))}, 'period')

        # NO PAST
        period = MonthPeriod.find_create_from(year=self.get('year'), \
                                                  month=self.get('month'))

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
            self.errors.add(_(u"The reporting time frame for that " \
                              "period (%(period)s) is over.") \
                            % {'period': period}, 'period')

        # DATE DAY / MONTH / YEAR
        try:
            date(self.get('fillin_year'), \
                 self.get('fillin_month'), self.get('fillin_day'))
        except ValueError:
            self.errors.add(_(u"The fillin day (%(day)s) is out of range " \
                            "for that month (%(month)s)") \
                            % {'day': \
                                   self.get('fillin_day').__str__().zfill(2), \
                               'month': \
                                self.get('fillin_month').__str__().zfill(2)}, \
                               'fillin')

        # ENTITY
        try:
            entity = Entity.objects.get(slug=self.get('hc'), \
                                        type__slug='cscom')
        except Entity.DoesNotExist:
            entity = None
            self.errors.add(_(u"The entity code (%(code)s) does not " \
                              "match any HC.") % {'code': \
                                                  self.get('hc')}, 'period')

        # NO DUPLICATE
        if not self.options.data_only:
            period = MonthPeriod.find_create_from(year=self.get('year'), \
                                                  month=self.get('month'))
            if entity \
            and MalariaReport.objects.filter(entity=entity, \
                                             period=period).count() > 0:
                report = MalariaReport.objects.get(entity=entity, period=period)
                self.errors.add(_(u"There is already a report for " \
                                  "that HC (%(entity)s) and that " \
                                  "period (%(period)s)") % \
                                  {'entity': entity.display_full_name(), \
                                   'period': period.name()}
                                   + u" Recu: %s." % report.receipt, 'period')

        # User can create such report
        if self.options.author:
            if not provider_can('can_submit_report', \
                                self.options.author, entity) \
               and not self.options.bulk_import:
                self.errors.add(_(u"You don't have permission to send " \
                                  "a report for that " \
                                  "location (%(loc)s).") \
                                % {'loc': entity.display_full_name()})


class RHCommoditiesReportValidator(DataValidator):

    """ Monthly RHCommodities Routine Report from CSCOM data validation """

    def validate(self):
        """ Test whether attached data matches PNLP's logic requirements """

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
            self.errors.add(_(u"The period of data (%(period)s) " \
                            "is in the future.") % \
                            {'period': u"%s %d" % \
                                       (month.__str__().zfill(2), \
                                        year)}, 'period')

        # NO PAST
        period = MonthPeriod.find_create_from(year=year, \
                                                  month=month)

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
            self.errors.add(_(u"The reporting time frame for that " \
                              "period (%(period)s) is over.") \
                            % {'period': period}, 'period')

        # date DAY / MONTH / YEAR
        try:
            date(self.get('fillin_year'), \
                 self.get('fillin_month'), self.get('fillin_day'))
        except ValueError:
            self.errors.add(_(u"The fillin day (%(day)s) is out of range " \
                            "for that month (%(month)s)") \
                            % {'day': \
                                   self.get('fillin_day').__str__().zfill(2), \
                               'month': \
                                self.get('fillin_month').__str__().zfill(2)}, \
                               'fillin')

        # ENTITY
        try:
            entity = Entity.objects.get(slug=self.get('entity'), \
                                        type__slug='cscom')
        except Entity.DoesNotExist:
            entity = None
            self.errors.add(_(u"The entity code (%(code)s) does not " \
                              "match any HC.") % {'code': \
                                                  self.get('entity')}, 'period')

        # NO DUPLICATE
        if not self.options.data_only:
            period = MonthPeriod.find_create_from(year=year, \
                                                  month=month)
            if entity \
            and RHCommoditiesReport.objects.filter(entity=entity, \
                                             period=period).count() > 0:
                report = RHCommoditiesReport.objects.get(entity=entity, \
                                                         period=period)
                self.errors.add(_(u"There is already a report for " \
                                  "that HC (%(entity)s) and that " \
                                  "period (%(period)s)") % \
                                  {'entity': entity.display_full_name(), \
                                   'period': period.name()}
                                   + u" Recu: %s." % report.receipt, 'period')

        # User can create such report
        if self.options.author:
            if not provider_can('can_submit_report', \
                                self.options.author, entity) \
               and not self.options.bulk_import:
                self.errors.add(_(u"You don't have permission to send " \
                                  "a report for that " \
                                  "location (%(loc)s).") \
                                % {'loc': entity.display_full_name()})


class EpidemiologyReportValidator(DataValidator):

    """ Monthly RHCommodities Routine Report from CSCOM data validation """

    def validate(self):
        """ Test whether attached data matches PNLP's logic requirements """

        no_more_than_text = _("%(field2)s (%(f2value)d) can't be more " \
                            "than %(field1)s (%(f1value)d)")

        def test_value_under(fieldref, fieldtest):
            try:
                dic = {'field2': self.field_name('%s' \
                                                 % (fieldtest)), \
                       'f2value': self.get('%s' % (fieldtest)), \
                       'field1': self.field_name('%s' \
                                                 % (fieldref)), \
                       'f1value': self.get('%s' % (fieldref))}
                if dic['f1value'] < dic['f2value']:
                    self.errors.add(no_more_than_text % dic)
            except MissingData:
                # this missing data should have already been reported
                pass

        # case > death
        test_value_under('acute_flaccid_paralysis_case', \
                         'acute_flaccid_paralysis_death')

        # case > death
        test_value_under('influenza_a_h1n1_case', \
                         'influenza_a_h1n1_death')

        # case > death
        test_value_under('cholera_case', \
                         'cholera_death')

        # case > death
        test_value_under('red_diarrhea_case', \
                         'red_diarrhea_death')

        # case > death
        test_value_under('measles_case', \
                         'measles_death')

        # case > death
        test_value_under('yellow_fever_case', \
                         'yellow_fever_death')

        # case > death
        test_value_under('neonatal_tetanus_case', \
                         'neonatal_tetanus_death')
        # case > death
        test_value_under('meningitis_case', \
                         'meningitis_death')
        # case > death
        test_value_under('rabies_case', \
                         'rabies_death')
        # case > death
        test_value_under('acute_measles_diarrhea_case', \
                         'acute_measles_diarrhea_death')
        # case > death
        test_value_under('other_notifiable_disease_case', \
                         'other_notifiable_disease_death')

        # PERIOD MONTH
        # range(1, 12)
        # already handled.

        # PERIOD YEAR
        # range(2010, 2020)
        # already handled

        # NO FUTURE
        year = self.get('reporting_year')
        week = self.get('reporting_week')
        if year >= date.today().year \
           and week >= date.today().isocalendar()[1]:
            self.errors.add(_(u"The period of data (%(period)s) " \
                            "is in the future.") % \
                            {'period': u"%s %d" % \
                                       (week.__str__().zfill(2), \
                                        year)}, 'period')

        # NO PAST
        period = WeekPeriod.find_create_by_weeknum(year, week)

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
            self.errors.add(_(u"The reporting time frame for that " \
                              "period (%(period)s) is over.") \
                            % {'period': period}, 'period')

        # date DAY / MONTH / YEAR
        try:
            date(self.get('fillin_year'), \
                 self.get('fillin_month'), self.get('fillin_day'))
        except ValueError:
            self.errors.add(_(u"The fillin day (%(day)s) is out of range " \
                            "for that month (%(month)s)") \
                            % {'day': \
                                   self.get('fillin_day').__str__().zfill(2), \
                               'month': \
                                self.get('fillin_month').__str__().zfill(2)}, \
                               'fillin')

        # ENTITY
        try:
            entity = Entity.objects.get(slug=self.get('location'), \
                                        type__slug='cscom')
        except Entity.DoesNotExist:
            entity = None
            self.errors.add(_(u"The entity code (%(code)s) does not " \
                              "match any HC.") % {'code': \
                                                  self.get('location')}, \
                                                  'period')

        # NO DUPLICATE
        if not self.options.data_only:
            period = WeekPeriod.find_create_by_weeknum(year, week)
            if entity \
            and EpidemiologyReport.objects.filter(entity=entity, \
                                             period=period).count() > 0:
                report = EpidemiologyReport.objects.get(entity=entity, \
                                                        period=period)
                self.errors.add(_(u"There is already a report for " \
                                  "that HC (%(entity)s) and that " \
                                  "period (%(period)s)") % \
                                  {'entity': entity.display_full_name(), \
                                   'period': period.name()}
                                   + u" Recu: %s." % report.receipt, 'period')

        # User can create such report
        if self.options.author:
            if not provider_can('can_submit_report', \
                                self.options.author, entity) \
               and not self.options.bulk_import:
                self.errors.add(_(u"You don't have permission to send " \
                                  "a report for that " \
                                  "location (%(loc)s).") \
                                % {'loc': entity.display_full_name()})
