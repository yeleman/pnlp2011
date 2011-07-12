#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import datetime, date, timedelta

from django import forms
from django.utils.translation import ugettext as _

from bolibana_auth.models import Access, Provider
from bolibana_reporting.models import MonthPeriod
from pnlp_core.models.MalariaReport import MalariaReport


class MalariaReportForm(forms.ModelForm):
    class Meta:
        model = MalariaReport
        exclude = ('_status', 'type', 'receipt', 'period', \
                   'entity', 'created_by', 'created_on', \
                   'modified_by', 'modified_on')


class MalariaDataHolder(object):

    def get(self, slug):
        return getattr(self, slug)

    def field_name(self, slug):
        return MalariaReport._meta.get_field(slug).verbose_name

    def set(self, slug, data):
        try:
            setattr(self, slug, data)
        except AttributeError:
            exec 'self.%s = None' % slug
            setattr(self, slug, data)

    def fields_for(self, cat):
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
                    'stockout_artemether', \
                    'stockout_quinine', \
                    'stockout_serum', \
                    'stockout_bednet', \
                    'stockout_rdt', \
                    'stockout_sp']

    def data_for_cat(self, cat, as_dict=False):
        data = []
        for field in self.fields_for(cat):
            data.append(self.get(field))
        return data


def current_period():
    """ Period of current date """
    return MonthPeriod.find_create_by_date(date.today())


def current_reporting_period():
    """ Period of reporting period applicable (last month) """
    return current_period().previous()


def provider_entity(provider):
    """ Entity a Provider is attached to """
    return provider.first_access().target


def get_reports_to_validate(entity, period=current_reporting_period()):
    """ List of Entity which have sent report but are not validated """
    return [(report.entity, report) \
            for report \
            in MalariaReport.unvalidated\
                            .filter(entity__in=entity.get_children(), \
                                    period=period)]


def get_validated_reports(entity, period=current_reporting_period()):
    """ List of all Entity which report have been validated """
    return [(report.entity, report) \
            for report \
            in MalariaReport.validated\
                            .filter(entity__in=entity.get_children(), \
                                    period=period)]


def get_not_received_reports(entity, period=current_reporting_period()):
    """ List of all Entity which have not send in a report """
    units = list(entity.get_children().all())
    reports = MalariaReport.objects.filter(entity__in=entity.get_children(), \
                                           period=period)
    for report in reports:
        units.remove(report.entity)
    return units


def time_over_by_delta(delta, period=current_period()):
    """ whether current date + delta is past """
    today = date.today()
    return date.fromtimestamp(float(period.end_on.strftime('%s'))) \
                              + delta <= today


def time_cscom_over(period=current_period()):
    """ time_over_by_delta() with cscom delta """
    return time_over_by_delta(timedelta(days=6), period)


def time_district_over(period=current_period()):
    """ time_over_by_delta() with district delta """
    return time_over_by_delta(timedelta(days=16), period)


def time_region_over(period=current_period()):
    """ time_over_by_delta() with region delta """
    return time_over_by_delta(timedelta(days=26), period)


def time_can_validate(entity):
    """ is it possible to do validation now for that entity? """
    level = entity.type.slug
    if level == 'district':
        return not time_district_over()
    if level == 'region':
        return not time_region_over()
    return False


def contact_for(entity, recursive=True):
    """ contact person for an entity. first found at level or sup levels """
    ct, oi = Access.target_data(entity)
    providers = Provider.objects\
                        .filter(access__in=Access.objects\
                                                 .filter(content_type=ct, \
                                                         object_id=oi))
    if providers.count() == 1:
            return providers.all()[0]
    if providers.count() > 0:
        return providers.all()[0]
    if entity.parent and recursive:
        return contact_for(entity.parent)
    return None


def most_accurate_report(provider, period=current_reporting_period()):
    # don't use that anymore I think
    try:
        return MalariaReport.validated.filter(period=period)[0]
    except:
        return None


def raw_data_periods_for(entity):
    """ periods with validated report for an entity """
    return [r.mperiod for r in MalariaReport.validated.filter(entity=entity)]


def entities_path(root, entity):
    """ [] or {} for multi-select containing path to root entity """
    paths = []
    if entity.get_children():
        p = {'selected': None, 'elems': entity_children(entity)}
        paths.append(p)
    while entity.parent and not entity == root:
        p = {'selected': entity.slug, 'elems': entity_children(entity.parent)}
        paths.append(p)
        entity = entity.parent
    paths.reverse()
    return paths


def entity_children(entity):
    """ (entity.slug, entity) of all children of an entity """
    return [(e.slug, e) for e in entity.children.all().order_by('name')]


def provider_can(permission, provider, entity=None):
    """ bolean if(not) provider has permission on entity or descendants """
    from bolibana_auth.models import Permission

    for access in provider.access.all():
        if access.role.permissions.filter(slug=permission).count() > 0:
            # provider as access. Not entity was queried.
            if entity == None:
                return True

            # if entity was queried, we need to find out if entity is
            # within the descendants of provider's one.
            if entity == access.target \
            or entity in access.target.get_descendants():
                return True
    return False


def provider_can_or_403(permission, provider, entity):
    """ returns provider_can() or raise Http403 """
    from pnlp_web.http import Http403
    if provider_can(permission, provider, entity):
        return True
    else:
        if entity:
            message = _(u"You don't have permission %(perm)s on %(entity)s") \
                      % {'perm': permission, \
                         'entity': entity.display_full_name()}
        else:
            message = _(u"You don't have permission %(perm)s") \
                      % {'perm': permission}
        raise Http403(message)
