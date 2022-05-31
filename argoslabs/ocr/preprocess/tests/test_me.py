
"""
====================================
 :mod:`argoslabs.ocr.preprocess`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/05/31]
#     - starting

################################################################################
import os
import sys
import glob
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from argoslabs.ocr.preprocess import _main as main
from contextlib import contextmanager
from io import StringIO


################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        os.chdir(os.path.dirname(__file__))
        self.assertTrue(True)
        # if os.path.exists(Tesseract.DATADIRS[1]):
        #     shutil.rmtree(Tesseract.DATADIRS[1])
        # self.assertTrue(not os.path.exists(Tesseract.DATADIRS[1]))

    # ==========================================================================
    def test0010_failure(self):
        try:
            r = main('-vvv')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0020_failure(self):
        try:
            r = main('invalid')
            self.assertTrue(r == 1)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0100_success_version(self):
        try:
            if os.path.exists('02-01.result.jpg'):
                os.remove('02-01.result.jpg')
            with captured_output() as (out, err):
                r = main('02-01.jpg', '--save-temp')
            self.assertTrue(r == 0)
            rs = out.getvalue()
            self.assertTrue(rs == os.path.abspath('02-01.result.jpg'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # # ==========================================================================
    # def test0110_success_version(self):
    #     try:
    #         if os.path.exists('02-02.res.jpg'):
    #             os.remove('02-02.res.jpg')
    #         with captured_output() as (out, err):
    #             r = main('02-02.jpg', '--target-image', '02-02.res.jpg')
    #         self.assertTrue(r == 0)
    #         rs = out.getvalue()
    #         self.assertTrue(rs == os.path.abspath('02-02.res.jpg'))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0120_success_version(self):
    #     try:
    #         if os.path.exists('02-10.result.jpg'):
    #             os.remove('02-10.result.jpg')
    #         with captured_output() as (out, err):
    #             r = main('02-10.jpg')
    #         self.assertTrue(r == 0)
    #         rs = out.getvalue()
    #         self.assertTrue(rs == os.path.abspath('02-10.result.jpg'))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # # ==========================================================================
    # def test0200_success_version(self):
    #     try:
    #         for f in glob.glob('receipts/IMG_????.jpeg'):
    #             with captured_output() as (out, err):
    #                 r = main(f, '--save-temp')
    #             self.assertTrue(r == 0)
    #             rs = out.getvalue()
    #             fn, ext = os.path.splitext(os.path.abspath(f))
    #             self.assertTrue(f'{fn}.result{ext}' == rs)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
