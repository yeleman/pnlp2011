#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import xlwt
import StringIO

borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1

font = xlwt.Font()
font.bold = True
font.height = 10 * 0x14

al = xlwt.Alignment()
al.horz = xlwt.Alignment.HORZ_CENTER
al.vert = xlwt.Alignment.VERT_CENTER

pat = xlwt.Pattern()
pat.pattern = xlwt.Pattern.SOLID_PATTERN
pat.pattern_fore_colour = 0x01F

colortitle = xlwt.Pattern()
colortitle.pattern = xlwt.Pattern.SOLID_PATTERN
colortitle.pattern_fore_colour = 0x01B

style = xlwt.XFStyle()
style.pattern = pat
style.borders = borders

styleb = xlwt.XFStyle()
styleb.borders = borders

styletitle = xlwt.XFStyle()
styletitle.pattern = colortitle
styletitle.borders = borders
styletitle.font = font
styletitle.alignment = al


def report_as_excel(report):
    ''' Export data '''

    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet(u"Report")

    sheet.col(0).width = 0x0d00 * 3
    sheet.write_merge(0, 0, 0, 15, u"Formulaire de Collecte - Données"\
                     u"sur l'Information de Routime du PNLP - Niveau" \
                     u"District Sanitaire (Csréf/Cscom)")
    sheet.write_merge(1, 4, 0, 0, u"Région Médical \nDistrict"\
                        u"Sanitaire \n \nEtablissement sanitaire", style)
    sheet.write_merge(5, 6, 0, 1, u"Classification", styletitle)
    sheet.write_merge(7, 7, 0, 1, u"Total consultation, toutes" \
                                     u"causes confondues", styleb)
    sheet.write_merge(8, 8, 0, 1, u"Nbre de Cas de paludisme"\
                                    u"(Tous suspectés)", styleb)
    sheet.write_merge(9, 9, 0, 1, u"Nbre de Cas de paludisme Simple",\
                                                                styleb)
    sheet.write_merge(10, 10, 0, 1, u"Nbre de Cas de paludisme Grave",\
                                                                styleb)
    sheet.write_merge(11, 11, 0, 1, u"Cas de paludisme testés"\
                                    u"(GE et/ou TDR)", styleb)
    sheet.write_merge(12, 12, 0, 1, u"Cas de paludisme confirmés"\
                                    u"(GE et/ou TDR)", styleb)
    sheet.write_merge(13, 13, 0, 1, u"Nbre de Cas traités avec CTA",\
                                                                styleb)
    sheet.write_merge(14, 14, 0, 15, u"")
    sheet.write_merge(15, 16, 0, 1, u"Classification", styletitle)
    sheet.write_merge(17, 17, 0, 1, u"Total Hospitalisations toutes"\
                                    u"causes confondues", styleb)
    sheet.write_merge(18, 18, 0, 1, u"Total Hospitalisés Paludisme",\
                                                                styleb)
    sheet.write_merge(19, 19, 0, 15, u"")
    sheet.write_merge(20, 21, 0, 1, u"Classification", styletitle)
    sheet.write_merge(22, 22, 0, 1, u"Total cas de décès toutes causes"\
                                    u"confondues", styleb)
    sheet.write_merge(23, 23, 0, 1, u"Cas de décès pour paludisme",\
                                                                styleb)
    sheet.write_merge(24, 24, 0, 15, u"")
    sheet.write_merge(25, 25, 0, 6, u"Moustiquaires imprégnées"\
                                u"d'insecticide distribuées", styletitle)
    sheet.write_merge(26, 26, 0, 1, u"Classification", styleb)
    sheet.write_merge(27, 27, 0, 1, u"Nombre de moustiquaires"\
                                            u"distribuées", styleb)
    sheet.write_merge(28, 29, 0, 15, u"")

    sheet.write(1, 1, u"Name Region")
    sheet.write(2, 1, u"Name district")
    sheet.write_merge(3, 4, 1, 2, u"Name cscom", styleb)

    sheet.write(2, 2, u"Mois")
    sheet.write(2, 3, u"6", styleb)
    sheet.write_merge(5, 5, 2, 6, u"Consultation", styletitle)
    sheet.write_merge(6, 6, 2, 3, u"< 5 ans ", styletitle)
    sheet.write_merge(6, 6, 4, 5, u"5 ans et plus",\
                                                            styletitle)
    sheet.write_merge(6, 6, 6, 7, u"Femmes enceintes", styletitle)

    sheet.write(2, 4, u"Année")
    sheet.write(2, 5, u"2011", styleb)

    stream = StringIO.StringIO()
    book.save(stream)

    return stream
