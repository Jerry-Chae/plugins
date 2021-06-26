"""
====================================
 :mod:`argoslabs.python.dynamic.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
#
# Authors
# ===========
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/03/30]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
from argoslabs.python.dynamic import _main as main

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
    # ==========================================================================
    def setUp(self) -> None:
        mdir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(mdir)

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_hello_01(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            pyf = 'hello-01.py'
            with captured_output() as (out, err):
                r = main(pyf)
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == 'Hello World!')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_hello_02(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            pyf = 'hello-02.py'
            with captured_output() as (out, err):
                r = main(pyf, '--params', 'name::=Jerry')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == 'Hello Jerry!')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_add_02(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            pyf = 'add-03.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--params', 'i::=123',
                    '--params', 'j::=10',
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == '133')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_task_1(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            pyf = 'task1.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--reqtxt', 'requirements.txt',
                    '--params', 'wdir::=%s' % os.getcwd(),
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == os.path.abspath(os.path.join(
                os.getcwd(), 'task1.xlsx'
            )))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_task_1_err_req(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            pyf = 'task1.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--reqtxt', 'req-err.txt',
                    '--params', 'wdir::=%s' % os.getcwd(),
                )
            self.assertTrue(r == 9)
            _err = err.getvalue()
            self.assertTrue(_err == 'Error: pip install with "req-err.txt" failure!')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_task_2(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            pyf = 'task2.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--reqtxt', 'requirements.txt',
                    '--params', 'wdir::=%s' % os.getcwd(),
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == os.path.abspath(os.path.join(
                os.getcwd(), 'task2.xlsx'
            )))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_scrapy_mike(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            #pyf = 'Webscrape_Argos_Jerry.py'
            pyf = 'scrape.py'
            odir = os.path.join(os.path.abspath('.'), 'output')
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--reqtxt', 'req-scrapy.txt',
                    '--params', 'searches::=["machine learning", "brain", "food", "robot"]',
                    '--params', 'input::=companies-10.csv',
                    '--params', f'output_folder::={odir}'
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            out.seek(0)
            rows = list()
            cr = csv.reader(out)
            for row in cr:
                rows.append(row)
                self.assertTrue(len(row) in (4,))
            self.assertTrue(rows[-1][1] == 'https://www.vicarious.com/')

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_scrapy_mike(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            pyf = 'Webscrape_Argos_Jerry.py'
            odir = os.path.join(os.path.abspath('.'), 'output')
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--reqtxt', r'W:\crpa_src\Bots\DynamicPythonScrapyMike\req-scrapy.txt',
                    '--params', "searches::=['machine learning', 'brain', 'food', 'robot']",
                    '--params', r'input::=W:\crpa_src\Bots\DynamicPythonScrapyMike\companies-10.csv',
                    '--params', f'output_folder::=C:\Temp\output'
                )
            self.assertTrue(r == 0)
            csv_f = out.getvalue()
            with open(csv_f, encoding='utf-8') as ifp:
                rows = list()
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
                    self.assertTrue(len(row) in (4,))
                self.assertTrue(rows[-1][1] in
                                ('https://www.vicarious.com/',
                                 'https://misorobotics.com/'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
