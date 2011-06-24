#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.utils.translation import ugettext_lazy as _, ugettext
from bolibana_reporting.excel import (ExcelForm, ExcelFormField, \
                                      ExcelTypeConverter)
from bolibana_reporting.models import Period, MonthPeriod, Entity
from pnlp_core.models import MalariaReport
from pnlp_core.validators import MalariaReportValidator


class MalariaExcelForm(ExcelForm):

    """ Mapping between MalariaReport & Excel Monthly Malaria Routine File """

    YN_MAP = {'oui': MalariaReport.YES, 'non': MalariaReport.NO}
    MONTH_MAP = range(1, 13)
    YEAR_MAP = range(2010, 2021)
    DAY_MAP = range(1, 32)

    _mapping = {'0.3': {
    'region': ExcelFormField('B2', unicode, _(u"Region")),
    'district': ExcelFormField('B3', unicode, _(u"Health District")),
    'hc': ExcelFormField('B4', unicode, _(u"Health Center")),
    'month': ExcelFormField('D3', ExcelTypeConverter.NormalizedIntChoiceList, \
                            _(u"Month"), cast_args=MONTH_MAP),
    'year': ExcelFormField('G3', ExcelTypeConverter.NormalizedIntChoiceList, \
                           _(u"Year"), cast_args=YEAR_MAP),

    'u5_total_consultation_all_causes': ExcelFormField('C7', int, \
                                        MalariaReport._meta.get_field(\
                           'u5_total_consultation_all_causes').verbose_name), \
    'o5_total_consultation_all_causes': ExcelFormField('E7', int, \
                                        MalariaReport._meta.get_field(\
                           'o5_total_consultation_all_causes').verbose_name), \
    'pw_total_consultation_all_causes': ExcelFormField('G7', int, \
                                        MalariaReport._meta.get_field(\
                           'pw_total_consultation_all_causes').verbose_name), \

    'u5_total_suspected_malaria_cases': ExcelFormField('C8', int, \
                                        MalariaReport._meta.get_field(\
                           'u5_total_suspected_malaria_cases').verbose_name), \
    'o5_total_suspected_malaria_cases': ExcelFormField('E8', int, \
                                        MalariaReport._meta.get_field(\
                           'o5_total_suspected_malaria_cases').verbose_name), \
    'pw_total_suspected_malaria_cases': ExcelFormField('G8', int, \
                                        MalariaReport._meta.get_field(\
                           'pw_total_suspected_malaria_cases').verbose_name), \

    'u5_total_simple_malaria_cases': ExcelFormField('C9', int, \
                                     MalariaReport._meta.get_field(\
                              'u5_total_simple_malaria_cases').verbose_name), \
    'o5_total_simple_malaria_cases': ExcelFormField('E9', int, \
                                     MalariaReport._meta.get_field(\
                              'o5_total_simple_malaria_cases').verbose_name), \

    'u5_total_severe_malaria_cases': ExcelFormField('C10', int, \
                                     MalariaReport._meta.get_field(\
                              'u5_total_severe_malaria_cases').verbose_name), \
    'o5_total_severe_malaria_cases': ExcelFormField('E10', int, \
                                     MalariaReport._meta.get_field(\
                              'o5_total_severe_malaria_cases').verbose_name), \
    'pw_total_severe_malaria_cases': ExcelFormField('G10', int, \
                                     MalariaReport._meta.get_field(\
                              'pw_total_severe_malaria_cases').verbose_name), \

    'u5_total_tested_malaria_cases': ExcelFormField('C11', int, \
                                     MalariaReport._meta.get_field(\
                              'u5_total_tested_malaria_cases').verbose_name), \
    'o5_total_tested_malaria_cases': ExcelFormField('E11', int, \
                                     MalariaReport._meta.get_field(\
                              'o5_total_tested_malaria_cases').verbose_name), \
    'pw_total_tested_malaria_cases': ExcelFormField('G11', int, \
                                     MalariaReport._meta.get_field(\
                              'pw_total_tested_malaria_cases').verbose_name), \

    'u5_total_confirmed_malaria_cases': ExcelFormField('C12', int, \
                                        MalariaReport._meta.get_field(\
                           'u5_total_confirmed_malaria_cases').verbose_name), \
    'o5_total_confirmed_malaria_cases': ExcelFormField('E12', int, \
                                        MalariaReport._meta.get_field(\
                           'o5_total_confirmed_malaria_cases').verbose_name), \
    'pw_total_confirmed_malaria_cases': ExcelFormField('G12', int, \
                                        MalariaReport._meta.get_field(\
                           'pw_total_confirmed_malaria_cases').verbose_name), \

    'u5_total_treated_malaria_cases': ExcelFormField('C13', int, \
                                      MalariaReport._meta.get_field(\
                             'u5_total_treated_malaria_cases').verbose_name), \
    'o5_total_treated_malaria_cases': ExcelFormField('E13', int, \
                                      MalariaReport._meta.get_field(\
                             'o5_total_treated_malaria_cases').verbose_name), \
    'pw_total_treated_malaria_cases': ExcelFormField('G13', int, \
                                      MalariaReport._meta.get_field(\
                             'pw_total_treated_malaria_cases').verbose_name), \

    'u5_total_inpatient_all_causes': ExcelFormField('C17', int, \
                                     MalariaReport._meta.get_field(\
                              'u5_total_inpatient_all_causes').verbose_name), \
    'o5_total_inpatient_all_causes': ExcelFormField('E17', int, \
                                     MalariaReport._meta.get_field(\
                              'o5_total_inpatient_all_causes').verbose_name), \
    'pw_total_inpatient_all_causes': ExcelFormField('G17', int, \
                                     MalariaReport._meta.get_field(\
                              'pw_total_inpatient_all_causes').verbose_name), \

    'u5_total_malaria_inpatient': ExcelFormField('C18', int, \
                                  MalariaReport._meta.get_field(\
                                 'u5_total_malaria_inpatient').verbose_name), \
    'o5_total_malaria_inpatient': ExcelFormField('E18', int, \
                                  MalariaReport._meta.get_field(\
                                 'o5_total_malaria_inpatient').verbose_name), \
    'pw_total_malaria_inpatient': ExcelFormField('G18', int, \
                                  MalariaReport._meta.get_field(\
                                 'pw_total_malaria_inpatient').verbose_name), \

    'u5_total_death_all_causes': ExcelFormField('C22', int, \
                                 MalariaReport._meta.get_field(\
                                  'u5_total_death_all_causes').verbose_name), \
    'o5_total_death_all_causes': ExcelFormField('E22', int, \
                                 MalariaReport._meta.get_field(\
                                  'o5_total_death_all_causes').verbose_name), \
    'pw_total_death_all_causes': ExcelFormField('G22', int, \
                                 MalariaReport._meta.get_field(\
                                  'pw_total_death_all_causes').verbose_name), \

    'u5_total_malaria_death': ExcelFormField('C23', int, \
                              MalariaReport._meta.get_field(\
                                     'u5_total_malaria_death').verbose_name), \
    'o5_total_malaria_death': ExcelFormField('E23', int, \
                              MalariaReport._meta.get_field(\
                                     'o5_total_malaria_death').verbose_name), \
    'pw_total_malaria_death': ExcelFormField('G23', int, \
                              MalariaReport._meta.get_field(\
                                     'pw_total_malaria_death').verbose_name), \

    'u5_total_distributed_bednets': ExcelFormField('C27', int, \
                                    MalariaReport._meta.get_field(\
                               'u5_total_distributed_bednets').verbose_name), \
    'pw_total_distributed_bednets': ExcelFormField('E27', int, \
                                    MalariaReport._meta.get_field(\
                               'pw_total_distributed_bednets').verbose_name), \

    'pw_total_anc1': ExcelFormField('M22', int, MalariaReport._meta.get_field(\
                                              'pw_total_anc1').verbose_name), \
    'pw_total_sp1': ExcelFormField('M23', int, MalariaReport._meta.get_field(\
                                               'pw_total_sp1').verbose_name), \
    'pw_total_sp2': ExcelFormField('M24', int, MalariaReport._meta.get_field(\
                                               'pw_total_sp2').verbose_name), \

    'stockout_act_children': ExcelFormField('M5', \
                                     ExcelTypeConverter.NormalizedChoiceList, \
                                     MalariaReport._meta.get_field(\
                                     'stockout_act_children').verbose_name, \
                                     cast_args=YN_MAP),
    'stockout_act_youth': ExcelFormField('M6', \
                                     ExcelTypeConverter.NormalizedChoiceList, \
                                     MalariaReport._meta.get_field(\
                                          'stockout_act_youth').verbose_name, \
                                     cast_args=YN_MAP),
    'stockout_act_adult': ExcelFormField('M7', \
                                     ExcelTypeConverter.NormalizedChoiceList, \
                                     MalariaReport._meta.get_field(\
                                          'stockout_act_adult').verbose_name, \
                                     cast_args=YN_MAP),
    'stockout_arthemeter': ExcelFormField('M11', \
                                     ExcelTypeConverter.NormalizedChoiceList, \
                                     MalariaReport._meta.get_field(\
                                         'stockout_arthemeter').verbose_name, \
                                     cast_args=YN_MAP),
    'stockout_quinine': ExcelFormField('M12', \
                                     ExcelTypeConverter.NormalizedChoiceList, \
                                     MalariaReport._meta.get_field(\
                                            'stockout_quinine').verbose_name, \
                                     cast_args=YN_MAP),
    'stockout_serum': ExcelFormField('M13', \
                                     ExcelTypeConverter.NormalizedChoiceList, \
                                     MalariaReport._meta.get_field(\
                                              'stockout_serum').verbose_name, \
                                     cast_args=YN_MAP),
    'stockout_bednet': ExcelFormField('M16', \
                                     ExcelTypeConverter.NormalizedChoiceList, \
                                     MalariaReport._meta.get_field(\
                                             'stockout_bednet').verbose_name, \
                                     cast_args=YN_MAP),
    'stockout_rdt': ExcelFormField('M17', \
                                     ExcelTypeConverter.NormalizedChoiceList, \
                                     MalariaReport._meta.get_field(\
                                                'stockout_rdt').verbose_name, \
                                     cast_args=YN_MAP),
    'stockout_sp': ExcelFormField('M18', \
                                     ExcelTypeConverter.NormalizedChoiceList, \
                                     MalariaReport._meta.get_field(\
                                                 'stockout_sp').verbose_name, \
                                     cast_args=YN_MAP),
    'fillin_day': ExcelFormField('K28', \
                                 ExcelTypeConverter.NormalizedIntChoiceList, \
                                 _(u"Filling Day"), cast_args=DAY_MAP),
    'fillin_month': ExcelFormField('L28', \
                                  ExcelTypeConverter.NormalizedIntChoiceList, \
                                  _(u"Filling Month"), cast_args=MONTH_MAP),
    'fillin_year': ExcelFormField('M28', \
                                  ExcelTypeConverter.NormalizedIntChoiceList, \
                                  _(u"Filling Year"), cast_args=YEAR_MAP),
    'author': ExcelFormField('L26', unicode, _(u"Author Name")),
        }
    }

    def section_from_variable(self, variable):
        """ slug section name from a variable slug """
        if variable.startswith('stockout_'):
            return 'stockout'
        last = variable.split('_', 1)[0]
        if last in ('u5', 'o5', 'pw'):
            return last
        if variable in ('month', 'year'):
            return 'period'
        if variable in ('region', 'district', 'hc'):
            return 'location'
        if variable.startswith('fillin_') or variable in ('author',):
            return 'fillin'
        return None

    def missing_value(self, variable):
        """ adds an error message for a missing value """
        self.errors.add(_("%(field)s is missing.") \
                        % {'field': self.mapping()[variable].display_name()}, \
                        self.section_from_variable(variable))

    def value_error(self, data, field, variable, exception):
        """ adds an error message for a value error """
        def clean_data(value):
            if isinstance(value, float) and value.is_integer():
                return int(value)
            return value

        self.errors.add(_("%(data)s is not a valid data for %(field)s") \
                        % {'data': clean_data(data), \
                           'field': field.display_name()}, \
                        self.section_from_variable(variable))

    def is_complete(self):
        """ Test all required fields for emptyness """
        blank_fields = ('region', 'district')
        complete = True
        for fieldid in self.mapping():
            if fieldid in blank_fields:
                continue

            try:
                value = self.get(fieldid)
            except MissingData:
                self.missing_value(fieldid)
                complete = False

            if value == None:
                self.missing_value(fieldid)
                complete = False
        return complete

    def validate(self):
        """ Triggers malaria routine Validator """
        validator = MalariaReportValidator(self)
        validator.errors.reset()
        validator.validate()
        self.errors.fusion(validator.errors)

    def fields_for(self, cat):
        """ list of variable slugs for a category name """
        u5fields = ['u5_total_consultation_all_causes', \
                    'u5_total_suspected_malaria_cases', \
                    'u5_total_simple_malaria_cases', \
                    'u5_total_severe_malaria_cases', \
                    'u5_total_tested_malaria_cases', \
                    'u5_total_confirmed_malaria_cases', \
                    'u5_total_treated_malaria_cases', \
                    'u5_total_inpatient_all_causes', \
                    'u5_total_malaria_inpatient', \
                    'u5_total_death_all_causes', \
                    'u5_total_malaria_death', \
                    'u5_total_distributed_bednets']
        if cat == 'u5':
            return u5fields
        if cat == 'o5':
            return [f.replace('u5', 'o5') for f in u5fields][:-1]
        if cat == 'pw':
            fields = [f.replace('u5', 'pw') for f in u5fields]
            fields.remove('pw_total_simple_malaria_cases')
            fields.extend(['pw_total_anc1', 'pw_total_sp1', 'pw_total_sp2'])
            return fields
        if cat == 'so':
            return ['stockout_act_children', \
                    'stockout_act_youth', \
                    'stockout_act_adult', \
                    'stockout_arthemeter', \
                    'stockout_quinine', \
                    'stockout_serum', \
                    'stockout_bednet', \
                    'stockout_rdt', \
                    'stockout_sp']

    def data_for_cat(self, cat, as_dict=False):
        """ Array of all values for a category. Arbitrary ordered """
        data = []
        for field in self.fields_for(cat):
            data.append(self.get(field))
        return data

    def create_report(self, author):
        """ creates and save a MalariaReport based on current data_browser

        No check nor validation is performed """
        period = MonthPeriod.find_create_from(year=self.get('year'), \
                                              month=self.get('month'))
        entity = Entity.objects.get(slug=self.get('hc'), type__slug='cscom')
        report = MalariaReport.start(period, entity, author, \
                                     type=MalariaReport.TYPE_SOURCE)

        report.add_underfive_data(*self.data_for_cat('u5'))
        report.add_overfive_data(*self.data_for_cat('o5'))
        report.add_pregnantwomen_data(*self.data_for_cat('pw'))
        report.add_stockout_data(*self.data_for_cat('so'))
        report.save()

        return report
