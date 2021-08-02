"""
====================================
 :mod:`argoslabs.data.excelstyle`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for Excel Style: unittest
"""
#
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2021/07/13]
#     - unittest
#  * [2021/07/13]
#     - starting
#


################################################################################
import os
import sys
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.data.excelstyle import _main as main


################################################################################
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test50_missing(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test100_samecol(self):
        try:
            r = main('new.xlsx', 'd1:d10', '--newfilename', 'new0.xlsx',
                     '--bold', '--italic', '--sheetname', 'Sheet1')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test150_diffcol(self):
        try:
            r = main('new.xlsx', 'a1:b10', '--newfilename', 'new0.xlsx',
                     '--bold', '--italic', '--underline', 'single',
                     '--sheetname', 'Sheet1')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test200_cell(self):
        try:
            r = main('new.xlsx', 'a1:h30', '--newfilename', 'new0.xlsx',
                     '--bold', '--italic', '--underline', 'double','--sheetname', 'Sheet1',
                     '--fillcolor','EE1111', '--operator', "!=",'--value','5')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

