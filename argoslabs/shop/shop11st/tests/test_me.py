"""
====================================
 :mod:`argoslabs.shop.shop11st.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Rossum API unittest module
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/03/10]
#     - starting

################################################################################
import os
import sys
from unittest import TestCase
from alabs.common.util.vvtest import captured_output
from argoslabs.shop.shop11st import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    key = '..'
    shop_id = 'SHOP_ID'

    # # ==========================================================================
    # def setUp(self) -> None:
    #     os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            with captured_output() as (out, err):
                r = main(self.key, self.shop_id)
            self.assertTrue(r == 0)
            _out = out.getvalue()
            print(_out)
            self.assertTrue(_out and _out.startswith('\nINSERT')
                            and _out.find('CBCI_11ST_GOODS') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
