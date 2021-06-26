"""
====================================
 :mod:`argoslabs.data.excelread`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
#
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#
#  * [2021/03/17]
#

################################################################################
import os
import sys
import csv
import shutil
import unittest
from tempfile import gettempdir
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.data.excelread import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    xlf = 'sample.xlsx'
    csv = 'foo.csv'
    wxl = os.path.join(gettempdir(), 'foo.xlsx')
    wcsv = os.path.join(gettempdir(), 'foo.csv')
    out = 'stdout.txt'
    err = 'stderr.txt'

        # ==========================================================================
    def test0800_excelreplace(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'A1:E4',
                     'apple',
                     'bab',
                     )
            self.assertTrue(r == 0)

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0810_excelreplace_blank(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'B3:E4',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0820_excelreplace_value(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     '',
                     'bab',
                     '',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0830_excelreplace_row(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'A1:B12',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0840_excelreplace_b2value(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'A1:B4',
                     ' abab',
                     ' bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0850_excelreplace_select_value(self):
        try:
            xls = "text_excel_data1.xlsx"
            r = main(xls,
                     'A',
                     'S1',
                     'Sol1',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0860_excelreplace_change_valueisnone(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     '--sheet', 'Sheet3',
                     '--data-only'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0870_excelreplace_row(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'A:B',
                     '',
                     'bab'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0880_excelreplace_sheet(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     '',
                     '',
                     'bab',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0890_excelreplace_range_none(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'A1:E4',
                     'apple',
                     'bab',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0900_write(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'E',
                     '',
                     'coding',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0910_range_one_cell(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'C1',
                     'banana',
                     'onecell',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0920_range_one_cell(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'C:D',
                     'banana',
                     'Strawberry',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0930_range(self):
        try:
            xls = "text_excel_data.xlsx"
            r = main(xls,
                     'B2:E19',
                     'banana',
                     'Strawberry',
                     '--sheet', 'Sheet2'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1000_CSV(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     'B1',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1010_CSV_Range_OneRow(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     'B',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1020_CSV_Range_Row(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     'B:D',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1030_CSV_Range_OneColumn(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     '2',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1040_CSV_Range_Column(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     '2:6',
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1050_CSV_Range_Select(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     '',
                     'bab',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1060_CSV_Range_OneColumn(self):
        try:
            xls = "text_excel.csv"
            r = main(xls,
                     '--range', '1:14'
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test1070_Shige_Debug(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            xls = r"C:\work\Bots\ExcelAdv\TestXLXS_0613.xlsx"
            r = main(xls,
                     '--sheet', 'Sheet1',
                     '--range', 'c1:d5',
                     '--data-only',
                     # '--outfile', self.out,
                     # '--errfile', self.err,
                     )
            self.assertTrue(r == 0)
            rr = []
            with open(self.out, 'r', encoding='utf8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    self.assertTrue(len(row) in (2,))
                    rr.append(row)
            self.assertTrue(len(rr) == 6)  # and rr[-1][-1] == '100100')

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        sg = sys.gettrace()
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        if os.path.exists(self.out):
            os.remove(self.out)
        if os.path.exists(self.err):
            os.remove(self.err)
        if os.path.exists(self.wxl):
            os.remove(self.wxl)
        if os.path.exists(self.wcsv):
            os.remove(self.wcsv)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
