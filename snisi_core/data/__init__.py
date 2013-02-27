#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import date, timedelta

from django.utils.translation import ugettext as _

from bolibana.models.Access import Access
from bolibana.models.Provider import Provider
from bolibana.models.Period import (MonthPeriod, WeekPeriod,
                                    QuarterPeriod, YearPeriod, DayPeriod)
from snisi_core.models.MalariaReport import MalariaR

COMMON_EXCLUDED_FIELDS = ('_status', 'type', 'receipt', 'period',
                          'entity', 'created_by', 'created_on',
                          'modified_by', 'modified_on')


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
    return [(report.entity, report)
            for report
            in MalariaR.unvalidated
                            .filter(entity__in=entity.get_children(),
                                    period=period)]


def get_validated_reports(entity, period=current_reporting_period()):
    """ List of all Entity which report have been validated """
    return [(report.entity, report) \
            for report \
            in MalariaR.validated\
                            .filter(entity__in=entity.get_children(),
                                    period=period)]


def get_not_received_reports(entity, period=current_reporting_period()):
    """ List of all Entity which have not send in a report """
    units = list(entity.get_children().all())
    reports = MalariaR.objects.filter(entity__in=entity.get_children(),
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
    return time_over_by_delta(timedelta(days=11), period)


def time_is_prompt(period=current_period()):
    """ returns True if it is in time """
    return not time_over_by_delta(timedelta(days=6), period)


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


def current_stage():
    period = current_reporting_period()
    if not time_cscom_over(period):
        return 'cscom'
    if not time_district_over(period):
        return 'district'
    if not time_region_over(period):
        return 'region'
    return 'over'


def contact_for(entity, recursive=True):
    """ contact person for an entity. first found at level or sup levels """
    ct, oi = Access.target_data(entity)
    providers = Provider.active\
                        .filter(access__in=Access.objects\
                                                 .filter(content_type=ct,
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
        return MalariaR.validated.filter(period=period)[0]
    except:
        return None


# def raw_data_periods_for(entity):
#     """ periods with validated report for an entity """
#     return [r.mperiod for r in MalariaR.validated.filter(entity=entity)]

def raw_data_periods_for(project, entity):
    """ periods with validated report for an entity and project """
    # return [r.mperiod for r in MalariaR.validated.filter(entity=entity)]
    src = [r.casted_period(project.get('period_cls'))
           for r in project.get('src_cls').validated.filter(entity=entity)]
    agg = [r.casted_period(project.get('period_cls'))
           for r in project.get('agg_cls').validated.filter(entity=entity)]
    return list(set(src + agg))


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
    from bolibana.web.http import Http403
    if provider_can(permission, provider, entity):
        return True
    else:
        if entity:
            message = _(u"You don't have permission %(perm)s on %(entity)s") \
                      % {'perm': permission,
                         'entity': entity.display_full_name()}
        else:
            message = _(u"You don't have permission %(perm)s") \
                      % {'perm': permission}
        raise Http403(message)


def period_from_url_str(period_str):

    year = indice = sub_indice = prefix = None

    def fail():
        raise ValueError(u"Incorrect period.")

    if not len(period_str):
        fail()

    if period_str.lower()[0] in ('q', 'w'):
        prefix = period_str.lower()[0]
        period_str = period_str[1:]


    parts = period_str.split('-')
    if not len(parts) in (1, 2, 3):
        fail()

    try:
        year = int(parts.pop())
        if len(parts):
            indice = int(parts.pop())

        if len(parts):
            sub_indice = int(parts.pop())

    except ValueError:
        fail()


    """
    FORMATS:

    YEAR:       2013                                [0-9]{4}
    MONTH:      01-2013                             [0-9]{2}-[0-9]{4}
    QUARTER:    Q1-2013                             Q[1-3]-[0-9]{4}
    WEEK:       W1-2013                             W[0-9]{1,2}-[0-9]{4}
    DAY:        01-01-2013                          [0-9]{2}-[0-9]{2}-[0-9]{4}
    """

    if sub_indice is not None:
        period = DayPeriod.find_create_from(year, indice, sub_indice)

    elif prefix == 'w':
        period = WeekPeriod.find_create_by_weeknum(year, indice)

    elif prefix == 'q':
        period = QuarterPeriod.find_create_by_quarter(year, indice)

    elif indice is not None:
        period = MonthPeriod.find_create_from(year, month=indice)

    else:
        period = YearPeriod.find_create_from(year)
    return period