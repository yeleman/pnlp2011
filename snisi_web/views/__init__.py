#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.http import Http404
from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _, ugettext_lazy
from django.conf import settings

from bolibana.web.decorators import provider_required
from bolibana.tools.utils import send_email

from snisi_core.projects import PROJECTS

# Malaria
import malaria

# SNISI
import generic_raw_data


def index(request):
    ''' Main Web Site Entry Point.

    Change it to redirect to appropriate default page '''
    return redirect(malaria.dashboard.dashboard)


def contact_choices(contacts):
    """ returns (a[0], a[1] for a in a list """
    # SUPPORT_CONTACTS contains slug, name, email
    # we need only slug, name for contact form.
    return [(slug, name) for slug, name, email in settings.SUPPORT_CONTACTS]


class ContactForm(forms.Form):
    """ Simple contact form with recipient choice """

    name = forms.CharField(max_length=50, required=True,
                                 label=ugettext_lazy(u"Your Name"))
    email = forms.EmailField(required=False,
                             label=ugettext_lazy(u"Your e-mail address"))
    phone_number = forms.CharField(max_length=12, required=False,
                                   label=ugettext_lazy(u"Your phone number"))
    subject = forms.CharField(max_length=50, required=False,
                                label=ugettext_lazy(u"Subject"))

    recipient = forms.ChoiceField(required=False,
                                  label=ugettext_lazy(u"Recipient"),
                          choices=contact_choices(settings.SUPPORT_CONTACTS),
                                  help_text=_(u"Choose PNLP for operational "
                                              u"requests and ANTIM for "
                                              u"technical ones."))

    message = forms.CharField(required=True,
                              label=ugettext_lazy(u"Your request"),
                              widget=forms.Textarea)


def contact(request):
    context = {'category': 'contact'}

    try:
        web_provider = request.user.get_profile()
    except:
        web_provider = None

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            try:
                dest_mail = [email for s, n, email
                                   in settings.SUPPORT_CONTACTS
                                   if s == 'pnlp'][0]
            except:
                dest_mail = []

            mail_cont = {'provider': web_provider,
                         'name': form.cleaned_data.get('name'),
                         'email': form.cleaned_data.get('email'),
                         'phone_number': form.cleaned_data.get('phone_number'),
                         'subject': form.cleaned_data.get('subject'),
                         'message': form.cleaned_data.get('message')}

            sent, sent_message = send_email(recipients=dest_mail,
                                            context=mail_cont,
                                        template='emails/support_request.txt',
                             title_template='emails/title.support_request.txt')
            if sent:
                messages.success(request, _(u"Support request sent."))
                return redirect('support')
            else:
                messages.error(request, _(u"Unable to send request. Please "
                                          "try again later."))

    if request.method == 'GET':
        if web_provider:
            initial_data = {'name': web_provider.name_access,
                          'email': web_provider.email,
                          'phone_number': web_provider.phone_number}
        else:
            initial_data = {}

        form = ContactForm(initial=initial_data)

    context.update({'form': form})

    return render(request, 'contact.html', context)


@provider_required
def generic_dashboard(request, project_slug):

    project = PROJECTS.get(project_slug)
    if project is None:
        raise Http404(_(u"Incorrect URL: Project Not Found."))

    submenu = '%s/submenu.html' % project.get('slug')

    context = {'category': project.get('category'),
               'location': 'dashboard',
               'project': project,
               'submenu': submenu}

    return render(request, 'dashboard.html', context)
