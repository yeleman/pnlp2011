#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin
# maintainer: Fad

import xlwt
import StringIO

# Définition des bordures
borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1

borderformbottom = xlwt.Borders()
borderformbottom.left = 0
borderformbottom.right = 0
borderformbottom.top = 0
borderformbottom.bottom = 2

borderformright = xlwt.Borders()
borderformright.left = 0
borderformright.right = 2
borderformright.top = 0
borderformright.bottom = 2

# Définition du font
font = xlwt.Font()
font.bold = True
font.height = 10 * 0x14

# On définit l'alignement
alcenter = xlwt.Alignment()
alcenter.horz = xlwt.Alignment.HORZ_CENTER
alcenter.vert = xlwt.Alignment.VERT_CENTER

# color
colordescription = xlwt.Pattern()
colordescription.pattern = xlwt.Pattern.SOLID_PATTERN
colordescription.pattern_fore_colour = 44

colordate = xlwt.Pattern()
colordate.pattern = xlwt.Pattern.SOLID_PATTERN
colordate.pattern_fore_colour = 0x01B

colortitle = xlwt.Pattern()
colortitle.pattern = xlwt.Pattern.SOLID_PATTERN
colortitle.pattern_fore_colour = 22

colorvide = xlwt.Pattern()
colorvide.pattern = xlwt.Pattern.SOLID_PATTERN
colorvide.pattern_fore_colour = 8

#style
styledescription = xlwt.XFStyle()
styledescription.pattern = colordescription

stylevariable = xlwt.XFStyle()
stylevariable.borders = borders
stylevariable.alignment = alcenter

styletitle = xlwt.XFStyle()
styletitle.pattern = colortitle
styletitle.borders = borders
styletitle.font = font
styletitle.alignment = alcenter

styledate = xlwt.XFStyle()
styledate.alignment = alcenter
styledate.pattern = colordate
styledate.borders = borders

stylelabel = xlwt.XFStyle()
stylelabel.borders = borders

stylevide = xlwt.XFStyle()
stylevide.pattern = colorvide
stylevide.alignment = alcenter

styleborformbutton = xlwt.XFStyle()
styleborformbutton.borders = borderformbottom

styleborformright = xlwt.XFStyle()
styleborformright.borders = borderformright

styletitleform = xlwt.XFStyle()
styletitleform.alignment = alcenter
styletitleform.borders = borders
styletitleform.font = font

styleentity = xlwt.XFStyle()
styleentity.borders = borders
styleentity.pattern = colortitle
styleentity.font = font


def report_as_excel(report):
    """ Export les données d'un rapport en xls """

    def report_status_verbose(value):
        for v, name in report.YESNO:
            if v.__str__() == value:
                return name.__unicode__()
        return value

    # On crée le doc xls
    book = xlwt.Workbook(encoding='utf-8')

    # On crée une feuille nommé Report
    sheet = book.add_sheet(u"Report")

    # J'agrandi la colonne à trois fois la normale.
    sheet.col(0).width = 0x0d00 * 3

    # Principe
    # write((nbre ligne - 1), nbre colonne, "contenu", style(optionnel).
    # write_merge((nbre ligne - 1), (nbre ligne - 1) + nbre de ligne
    # à merger, (nbre de colonne - 1), (nbre de colonne - 1) + nbre
    # de colonne à merger, u"contenu", style(optionnel)).
    sheet.write_merge(0, 0, 0, 12, u"Formulaire de Collecte - Données"\
                    u"sur l'Information de Routime du PNLP - Niveau" \
                    u"District Sanitaire (Csréf/Cscom)", styletitleform)
    sheet.write(1, 0, u"Région Médical", styledescription)
    sheet.write(2, 0, u"District Sanitaire", styledescription)
    sheet.write(3, 0, u"Etablissement sanitaire", styledescription)

    sheet.write_merge(4, 5, 0, 1, u"Classification", styletitle)
    sheet.write_merge(6, 6, 0, 1, u"Total consultation, toutes" \
                                     u"causes confondues", stylelabel)
    sheet.write_merge(7, 7, 0, 1, u"Nbre de Cas de paludisme"\
                                    u"(Tous suspectés)", stylelabel)
    sheet.write_merge(8, 8, 0, 1, u"Nbre de Cas de paludisme Simple",\
                                                            stylelabel)
    sheet.write_merge(9, 9, 0, 1, u"Nbre de Cas de paludisme Grave",\
                                                            stylelabel)
    sheet.write_merge(10, 10, 0, 1, u"Cas de paludisme testés"\
                                    u"(GE et/ou TDR)", stylelabel)
    sheet.write_merge(11, 11, 0, 1, u"Cas de paludisme confirmés"\
                                    u"(GE et/ou TDR)", stylelabel)
    sheet.write_merge(12, 12, 0, 1, u"Nbre de Cas traités avec CTA",\
                                                            stylelabel)
    sheet.write_merge(13, 13, 0, 12, u"")

    sheet.write_merge(14, 15, 0, 1, u"Classification", styletitle)
    sheet.write_merge(16, 16, 0, 1, u"Total Hospitalisations toutes"\
                                    u"causes confondues", stylelabel)
    sheet.write_merge(17, 17, 0, 1, u"Total Hospitalisés Paludisme",\
                                                            stylelabel)
    sheet.write_merge(18, 18, 0, 12, u"")

    sheet.write_merge(19, 20, 0, 1, u"Classification", styletitle)
    sheet.write_merge(21, 21, 0, 1, u"Total cas de décès toutes causes"\
                                    u"confondues", stylelabel)
    sheet.write_merge(22, 22, 0, 1, u"Cas de décès pour paludisme",\
                                                            stylelabel)
    sheet.write_merge(23, 23, 0, 9, u"")

    sheet.write_merge(24, 24, 0, 5, u"Moustiquaires imprégnées"\
                                u"d'insecticide distribuées", styletitle)

    sheet.write_merge(25, 25, 0, 1, u"Classification", styletitle)
    sheet.write_merge(26, 26, 0, 1, u"Nombre de moustiquaires"\
                                            u"distribuées", stylelabel)
    sheet.write_merge(27, 27, 0, 8, u"")
    sheet.write_merge(28, 28, 0, 12, u"", styleborformbutton)

    sheet.write(1, 1, report.entity.parent.parent.display_name(), \
                                                        styleentity)
    sheet.write(2, 1, report.entity.parent.display_name(), styleentity)
    sheet.write_merge(3, 3, 1, 2, report.entity.slug, styleentity)

    sheet.write_merge(1, 1, 2, 12, u"", styledescription)
    sheet.write(2, 2, u"Mois", styledescription)
    sheet.write(2, 3, report.period.middle().month, styledate)
    sheet.write(2, 4, u"", styledescription)
    sheet.write(2, 5, u"Année", styledescription)
    sheet.write(2, 6, report.period.middle().year, styledate)
    sheet.write_merge(2, 2, 7, 12, u"", styledescription)

    # SECTION Consultation
    sheet.write_merge(4, 4, 2, 7, u"Consultation", styletitle)

    # les données de < 5 ans
    sheet.write_merge(5, 5, 2, 3, u"< 5 ans", styletitle)
    sheet.write_merge(6, 6, 2, 3, \
                        report.u5_total_consultation_all_causes, \
                                                        stylevariable)
    sheet.write_merge(7, 7, 2, 3, \
                        report.u5_total_suspected_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(8, 8, 2, 3, \
                           report.u5_total_simple_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(9, 9, 2, 3, \
                           report.u5_total_severe_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(10, 10, 2, 3, \
                           report.u5_total_tested_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(11, 11, 2, 3, \
                        report.u5_total_confirmed_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(12, 12, 2, 3, \
                          report.u5_total_treated_malaria_cases, \
                                                        stylevariable)

    # les données de 5 ans et plus
    sheet.write_merge(5, 5, 4, 5, u"5 ans et plus", styletitle)
    sheet.write_merge(6, 6, 4, 5, \
                        report.o5_total_consultation_all_causes, \
                                                        stylevariable)
    sheet.write_merge(7, 7, 4, 5, \
                        report.o5_total_suspected_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(8, 8, 4, 5, \
                           report.o5_total_simple_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(9, 9, 4, 5, \
                           report.o5_total_severe_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(10, 10, 4, 5, \
                           report.o5_total_tested_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(11, 11, 4, 5, \
                        report.o5_total_confirmed_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(12, 12, 4, 5, \
                          report.o5_total_treated_malaria_cases, \
                                                        stylevariable)

    # les données des Femmes enceintes
    sheet.write_merge(5, 5, 6, 7, u"Femmes enceintes", styletitle)
    sheet.write_merge(6, 6, 6, 7, \
                        report.pw_total_consultation_all_causes, \
                                                        stylevariable)
    sheet.write_merge(7, 7, 6, 7, \
                        report.pw_total_suspected_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(8, 8, 6, 7, u"", stylevide)
    sheet.write_merge(9, 9, 6, 7, \
                           report.pw_total_severe_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(10, 10, 6, 7, \
                           report.pw_total_tested_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(11, 11, 6, 7, \
                        report.pw_total_confirmed_malaria_cases, \
                                                        stylevariable)
    sheet.write_merge(12, 12, 6, 7, \
                          report.pw_total_treated_malaria_cases, \
                                                        stylevariable)
    # SECTION Hospitalisations
    sheet.write_merge(14, 14, 2, 7, u"Hospitalisations", styletitle)
    # les données de < 5 ans
    sheet.write_merge(15, 15, 2, 3, u"< 5 ans", styletitle)
    sheet.write_merge(16, 16, 2, 3, \
                           report.u5_total_inpatient_all_causes, \
                                                        stylevariable)
    sheet.write_merge(17, 17, 2, 3, \
                              report.u5_total_malaria_inpatient, \
                                                        stylevariable)
    # + 5 ans
    sheet.write_merge(15, 15, 4, 5, u" + 5 ans", styletitle)
    sheet.write_merge(16, 16, 4, 5, \
                           report.o5_total_inpatient_all_causes, \
                                                        stylevariable)
    sheet.write_merge(17, 17, 4, 5, \
                              report.o5_total_malaria_inpatient, \
                                                        stylevariable)

    # les données des Femmes enceintes
    sheet.write_merge(15, 15, 6, 7, u"Femmes enceintes", styletitle)
    sheet.write_merge(16, 16, 6, 7, \
                           report.pw_total_inpatient_all_causes, \
                                                        stylevariable)
    sheet.write_merge(17, 17, 6, 7, \
                              report.pw_total_malaria_inpatient, \
                                                        stylevariable)

    # SECTION Decès
    sheet.write_merge(19, 19, 2, 7, u"Decès", styletitle)

    # * les données de < 5 ans
    sheet.write_merge(20, 20, 2, 3, u"< 5 ans", styletitle)
    sheet.write_merge(21, 21, 2, 3, \
                               report.u5_total_death_all_causes, \
                                                        stylevariable)
    sheet.write_merge(22, 22, 2, 3, report.u5_total_malaria_death, \
                                                                 \
                                                        stylevariable)

    # les données de 5 ans et plus
    sheet.write_merge(20, 20, 4, 5, u"5 ans et plus", styletitle)
    sheet.write_merge(21, 21, 4, 5, report.o5_total_death_all_causes, \
                                                        stylevariable)
    sheet.write_merge(22, 22, 4, 5, report.o5_total_malaria_death, \
                                                        stylevariable)

    # les données de Femmes enceintes
    sheet.write_merge(20, 20, 6, 7, u"Femmes enceintes", styletitle)
    sheet.write_merge(21, 21, 6, 7, report.pw_total_death_all_causes, \
                                                        stylevariable)
    sheet.write_merge(22, 22, 6, 7, report.pw_total_malaria_death, \
                                                        stylevariable)

    # SECTION Moustiquaires imprégnéés d'insecticide distrivuées
    # < 5 ans
    sheet.write_merge(25, 25, 2, 3, u"< 5 ans", styletitle)
    sheet.write_merge(26, 26, 2, 3, \
                            report.u5_total_distributed_bednets, \
                                                        stylevariable)
    sheet.write_merge(25, 25, 4, 5, u"Femmes enceintes", styletitle)
    sheet.write_merge(26, 26, 4, 5, \
                            report.pw_total_distributed_bednets, \
                                                        stylevariable)

    # SECTION Rupture de stock CTA pendant le mois (Oui, Non)
    sheet.write_merge(3, 3, 9, 12, u"Rupture de stock CTA pendant" \
                                   u"le mois \n (Oui, Non)", styletitle)
    sheet.write_merge(4, 4, 9, 11, u"CTA Nourisson - Enfant", stylelabel)
    sheet.write(4, 12, \
            report_status_verbose(report.stockout_act_children), \
                                                        stylevariable)
    sheet.write_merge(5, 5, 9, 11, u"CTA Adolescent", stylelabel)
    sheet.write(5, 12, \
               report_status_verbose(report.stockout_act_youth), \
                                                        stylevariable)
    sheet.write_merge(6, 6, 9, 11, u"CTA Adulte", stylelabel)
    sheet.write(6, 12, \
               report_status_verbose(report.stockout_act_adult), \
                                                        stylevariable)
    sheet.write_merge(7, 7, 8, 12, u"")

    # SECTION PEC de cas de Paludisme grave Rupture de soctk OUI/NON
    sheet.write_merge(8, 8, 9, 12, u"PEC de cas de Paludisme grave", \
                                                            styletitle)
    sheet.write_merge(9, 9, 9, 12, u"Rupture de soctk OUI/NON", \
                                                            styletitle)
    sheet.write_merge(10, 10, 9, 11, u"Arthemether injectable", stylelabel)
    sheet.write(10, 12, \
              report_status_verbose(report.stockout_artemether), \
                                                        stylevariable)
    sheet.write_merge(11, 11, 9, 11, u"Quinine Injectable", stylelabel)
    sheet.write(11, 12, report_status_verbose(report.stockout_quinine), \
                                                        stylevariable)
    sheet.write_merge(12, 12, 9, 11, u"Serum", stylelabel)
    sheet.write(12, 12, report_status_verbose(report.stockout_serum), \
                                                        stylevariable)

    # SECTION Rupture de stock pendant le mois O/N (Oui, Non)
    sheet.write_merge(14, 14, 10, 12, u"Rupture de stock pendant" \
                                      u" le mois O/N \n(Oui, Non)",\
                                       styletitle)
    sheet.write_merge(15, 15, 10, 11, u"MILD", stylelabel)
    sheet.write(15, 12, report_status_verbose(report.stockout_bednet), \
                                                        stylevariable)
    sheet.write_merge(16, 16, 10, 11, u"TDR", stylelabel)
    sheet.write(16, 12, report_status_verbose(report.stockout_rdt), \
                                                        stylevariable)
    sheet.write_merge(17, 17, 10, 11, u"SP", stylelabel)
    sheet.write(17, 12, report_status_verbose(report.stockout_sp), \
                                                        stylevariable)

    # SECTION CPN/SP des femme s enceintes (nbre)
    sheet.write_merge(19, 20, 10, 12, u"CPN/SP des femmes" \
                                      u"enceintes (nbre)", styletitleform)
    sheet.write_merge(21, 21, 10, 11, u"CPN 1", stylelabel)
    sheet.write(21, 12, report.pw_total_anc1, stylevariable)
    sheet.write_merge(22, 22, 10, 11, u"SP 1", stylelabel)
    sheet.write(22, 12, report.pw_total_sp1, stylevariable)
    sheet.write_merge(23, 23, 10, 11, u"SP 2", stylelabel)
    sheet.write(23, 12, report.pw_total_sp2, stylevariable)

    sheet.write(25, 9, u"Nom et Prénom :")
    sheet.write(25, 11, report.created_by.name())
    sheet.write(26, 9, u"Le Responsable CSCom/CSRéf")
    sheet.write(27, 9, u"Date :")
    sheet.write(27, 10, report.created_on.day, styledate)
    sheet.write(27, 11, report.created_on.month, styledate)
    sheet.write(27, 12, report.created_on.year, styledate)

    sheet.write_merge(0, 28, 13, 13, u"", styleborformright)

    if report.type == report.TYPE_AGGREGATED:
        sheet.write(35, 0, u"Sources", styletitle)
        i = 36
        for source in report.sources.all():
            sheet.write(i, 0, u"%s - %s" % \
                        (source.entity.display_name(), report.receipt),\
                                                            stylelabel)
            i += 1

    stream = StringIO.StringIO()
    book.save(stream)

    return stream
