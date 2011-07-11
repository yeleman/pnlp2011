#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import xlwt
import StringIO


def report_as_excel(report):

    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet(u"Report")
    sheet.write(0, 0, u"test")

    stream = StringIO.StringIO()
    book.save(stream)

    return stream
