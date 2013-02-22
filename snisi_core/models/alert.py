#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import logging
from datetime import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

logger = logging.getLogger(__name__)


class Options(dict, object):

    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)

    def __getattribute__(self, name):
        try:
            return self[name]
        except:
            return None


class Alert(models.Model):

    class Meta:
        app_label = 'snisi_core'

    alert_id = models.CharField(max_length=100, primary_key=True)
    created = models.DateTimeField(_(u"created"), auto_now_add=True)
    content_type = models.ForeignKey(ContentType)

    def __unicode__(self):
        return u"Alert.%(ct)s/%(id)s" \
               % {'ct': self.content_type.model.title(),
                  'id': self.alert_id}

    @classmethod
    def create(cls, *args, **kwargs):
        instance = cls(content_type=cls.get_ct(),
                       created=datetime.now())
        if not 'persist' in kwargs:
            kwargs['persist'] = True
        instance.args = Options(**kwargs)
        instance.alert_id = instance.get_alert_id()
        return instance

    def triggered(self):
        """ if this alert has been triggered (exists in DB) """
        return self.__class__.objects.filter(alert_id=self.get_alert_id(),
                                  content_type=self.content_type).count() > 0

    @property
    def aid(self):
        """ returns the generated Alert ID for use before creating alert """
        return self.get_alert_id()

    @property
    def not_triggered(self):
        """ shortcut property to know if alert has been triggered already """
        return not self.triggered()

    def can_trigger(self, *args, **kwargs):
        """ override this to set whether or not alert should be triggered """
        return False

    @classmethod
    def get_ct(cls):
        """ returns the ContentType for this class """

        ctype, created = ContentType.objects.get_or_create(
            app_label=cls._meta.app_label,
            model=cls._meta.object_name.lower(),
            defaults={'name': smart_unicode(cls._meta.verbose_name_raw)})

        return ctype

    def trigger(self, *args, **kwargs):
        """ call this to trigger your alert's action """
        try:
            self.action()
        except Exception as e:
            logger.error(u"%(alert)s raised %(e)r" % {'alert': self, 'e': e})
            raise
        else:
            if self.args.persist:
                self.save()

    def action(self):
        """ your code for that alert """
        pass

    def save(self, *args, **kwargs):
        if not self.alert_id:
            self.alert_id = self.get_alert_id()
        try:
            if not self.content_type:
                self.content_type = self.get_ct()
        except:
            self.content_type = self.get_ct()
        super(Alert, self).save(*args, **kwargs)
