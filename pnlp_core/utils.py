#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import smtplib

from django.core import mail
from django.conf import settings
from django.template import Template, loader, Context
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site, get_current_site


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
