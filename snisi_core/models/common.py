#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import reversion


def pre_save_report(sender, instance, **kwargs):
    """ change _status property of Report on save() at creation """
    if instance._status == instance.STATUS_UNSAVED:
        instance._status = instance.STATUS_CLOSED
    # following will allow us to detect failure in registration
    if not instance.receipt:
        instance.receipt = 'NO_RECEIPT'


def aggregated_model_report_pre_save(sender, instance, **kwargs):
    if instance.type == instance.TYPE_SOURCE:
        raise ValueError(u"This model (%s) cannot "
                         u"contain Source Reports." % sender)


def post_save_report(sender, instance, **kwargs):
    """ generates the receipt """
    if instance.receipt == 'NO_RECEIPT':
        instance.receipt = sender.generate_receipt(instance)
        instance.save()


def report_create_from(cls, period, entity, author, indiv_cls=None):
    """ Create An Aggregated report from Individual or Aggregated

        Report Class (cls) must obey to the conventional Report API:
        Subclass of Report
        cls.start()
        cls.indiv_sources = PosInt()
        cls.agg_sources = PosInt()
        cls.fill_blank() # if no sources
        cls.update_instance_with_indiv()
        cls.update_instance_with_agg() """

    # create empty
    agg_report = cls.start(entity=entity, period=period, author=author)
    agg_report.type = cls.TYPE_AGGREGATED
    agg_report.fill_blank()

    # find list of sources
    indiv_sources = indiv_cls.objects \
                             .filter(period=period,
                                     entity__in=entity.get_children())
    agg_sources = cls.objects.filter(period=period,
                                     entity__in=entity.get_children())

    sources = list(indiv_sources) + list(agg_sources)

    # loop on all sources
    for source in sources:
        if isinstance(source, indiv_cls):
            cls.update_instance_with_indiv(agg_report, source)
        elif isinstance(source, cls):
            cls.update_instance_with_agg(agg_report, source)

    # save to allow m2m
    agg_report.save()

    # keep a record of all sources
    for report in indiv_sources:
        agg_report.indiv_sources.add(report)

    for report in agg_sources:
        agg_report.agg_sources.add(report)

    with reversion.create_revision():
        agg_report.save()
        reversion.set_user(author)

    return agg_report
