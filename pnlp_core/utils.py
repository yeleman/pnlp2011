#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import smtplib
from datetime import datetime, date, timedelta

from django.core import mail
from django.conf import settings
from django.template import Template, loader, Context
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site, get_current_site

from bolibana_auth.models import Access, Provider
from bolibana_reporting.models import MonthPeriod
from pnlp_core.models import MalariaReport


def send_email(recipients, message=None, template=None, context={}, \
               title=None, title_template=None, sender=None):
    """ forge and send an email message

        recipients: a list of or a string email address
        message: string or template name to build email body
        title: string or title_template to build email subject
        sender: string otherwise EMAIL_SENDER setting
        content: a dict to be used to render both templates

        returns: (success, message)
            success: a boolean if connecion went through
            message: an int number of email sent if success is True
                     else, an Exception """

    if not isinstance(recipients, (list, tuple)):
        recipients = [recipients]

    # remove empty emails from list
    # might happen everytime a user did not set email address.
    try:
        while True:
            recipients.remove(u"")
    except ValueError:
        pass

    # no need to continue if there's no recipients
    if recipients.__len__() == 0:
        return (False, ValueError(_(u"No Recipients for that message")))

    # no body text forbidden. most likely an error
    if not message and not template:
        return (False, ValueError(_(u"Unable to send empty email messages")))

    # build email body. rendered template has priority
    if template:
        email_msg = loader.get_template(template).render(Context(context))
    else:
        email_msg = message

    # if no title provided, use default one. empty title allowed
    if title == None and not title_template:
        email_subject = _(u"Message from %(site)s") \
                        % {'site': Site.objects.get_current().name}

    # build email subject. rendered template has priority
    if title_template:
        email_subject = loader.get_template(title_template)\
                                                      .render(Context(context))
    elif title != None:
        email_subject = title

    # title can't contain new line
    email_subject = email_subject.strip()

    # default sender from config
    if not sender:
        sender = settings.EMAIL_SENDER

    try:
        #mail.send_mail(email_subject, email_msg, sender, \
        #          recipients, fail_silently=False)
        mail.send_mass_mail(((email_subject, email_msg, sender, recipients),), \
                            fail_silently=False)
        return (True, recipients.__len__())
    except smtplib.SMTPException as e:
        # log that error
        return (False, e)


def full_url(request=None):
    return 'http://%(domain)s/' % {'domain': get_current_site(request).domain}


def current_period():
    """ Period of current date """
    return MonthPeriod.find_create_by_date(date.today())


def current_reporting_period():
    """ Period of reporting period applicable (last month) """
    return current_period().previous()


def provider_entity(provider):
    """ Entity a Provider is attached to """
    return provider.default_access().target


def get_reports_to_validate(entity, period=current_reporting_period()):
    """ List of Entity which have sent report but are not validated """
    return [(report.entity, report) \
            for report \
            in MalariaReport.unvalidated.filter(entity__in=entity.get_children(), period=period)]


def get_validated_reports(entity, period=current_reporting_period()):
    """ List of all Entity which report have been validated """
    return [(report.entity, report) \
            for report \
            in MalariaReport.validated.filter(entity__in=entity.get_children(), period=period)]


def get_not_received_reports(entity, period=current_reporting_period()):
    """ List of all Entity which have not send in a report """
    units = list(entity.get_children().all())
    reports = MalariaReport.objects.filter(entity__in=entity.get_children(), \
                                           period=period)
    for report in reports:
        units.remove(report.entity)
    return units


def time_over_by_delta(delta):
    period = current_reporting_period().next()
    today = date.today()
    return date.fromtimestamp(float(period.start_on.strftime('%s'))) + delta <= today


def time_cscom_over():
    return time_over_by_delta(timedelta(days=5))


def time_district_over():
    return time_over_by_delta(timedelta(days=15))


def time_region_over():
    return time_over_by_delta(timedelta(days=25))


def time_can_validate(entity):
    level = entity.type.slug
    if level == 'district':
        return not time_district_over()
    if level == 'region':
        return not time_region_over()
    return False


def contact_for(entity):
    ct, oi = Access.target_data(entity)
    providers = Provider.objects.filter(access__in=Access.objects.filter(content_type=ct, object_id=oi))
    if providers.count() == 1:
            return providers.all()[0]
    if providers.count() > 0:
        return providers.all()[0]
    if entity.parent:
        return contact_for(entity.parent)
    return None
