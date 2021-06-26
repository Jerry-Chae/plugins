"""
====================================
 :mod:`argoslabs.api.coupang.tests.test_me`
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
#  * [2021/04/02]
#    - 특정 상품은 로켓배송이라 오류가 발생하는데 이 경우 그냥 넘어가도록 함
#  * [2021/02/10]
#     - CBCI_COUPANG_STOCK 의 'CONTENTS_TYPE_' 로 시작하는 컬럼들의 값이
#       'TEXT', 'TEXT_TEXT', 'TITLE'일 경우에만 'CONTESTS_DT_CONTENT_ ',
#       'CONTENTS_DT_ _DT_TYPE' 컬럼들에 값을 넣고 아니면 ''
#  * [2021/01/26]
#     - SQL에서 다음 정보 입력하는 데 문제
#       '<p><img src="http://image1.coupangcdn.com/image/vendor_inventory/cda2/3dd9a7c7b469cab575c6a437758ef99c07f4187622a967840e3370957fe5.png" title="202010181525289976.png"><br style="clear:both;"><img src="http://image1.coupangcdn.com/image/vendor_inventory/995e/97eb000144c92b464d6bd1a06287f7490c208bbddc9894627f44f742eb1d.png" title="202010181525308393.png"><br style="clear:both;"> </p>'
#       다음 다섯 입력 값을 base64 인코딩
#       CONTENTS_DT_1_CONTENT_1 = '{91}'
#       CONTENTS_DT_1_CONTENT_2 = '{94}'
#       CONTENTS_DT_1_CONTENT_3 = '{97}'
#       CONTENTS_DT_1_CONTENT_4 = '{100}'
#       CONTENTS_DT_1_CONTENT_5 = '{103}'
#  * [2021/01/20]
#     - &nbsp;, &quot; 등의 HTML 코드를 위한 SQL용으로 값 변환 넣음
#  * [2020/12/30]
#     - USER_NO 제외한 새로운 SQL 적용
#  * [2020/12/27]
#     - CBCI_COUPANG_STOCK 테이블 입력에 대한 새로운 SQL적용
#  * [2020/12/07]
#     - user_no, shop_id 패러미터 추가
#     - externalVendorSku 값에 따라 다음과 같이 넣도록 함
#       REPLACE INTO CBCI_COUPANG_STOCK VALUES ('USER_NO','SHOP_ID','USER_NO{16}'
#       REPLACE INTO CBCI_COUPANG_STOCK VALUES ('USER_NO','SHOP_ID',NULL'
#  * [2020/11/26]
#     - NOW() 는 값이 아니라 마지막에 따옴표 없이 넣도록 수정
#  * [2020/11/25]
#     - 각각의 플러그인 대신 하나의 SQL로 결과 나오도록 함
#  * [2020/11/15]
#     - 4개의 조회를 하나의 플러그인 으로
#  * [2020/10/30]
#     - starting

################################################################################
import os
import sys
import csv
from unittest import TestCase
from alabs.common.util.vvtest import captured_output
from argoslabs.shop.coupang import _main as main, OPS


################################################################################
class TU(TestCase):
    # ==========================================================================
    accesskey = ".."
    secretkey = ".."

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_invalid_param(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success_get_sql(self):
        os.chdir(os.path.dirname(__file__))
        try:
            vendor_id = 'A00118648'
            shop_id = 'voysis'

            with captured_output() as (out, err):
                r = main(self.accesskey, self.secretkey,
                         vendor_id, shop_id)
            self.assertTrue(r == 0)
            _out = out.getvalue()
            print(_out)
            out.seek(0)
            self.assertTrue(_out.find('441513480') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_debug(self):
        # [ID] ypa0940
        # [VENDER ID] A00010954
        # [API_KEY] df34fb44-167c-47f1-a3ea-21f703231302
        # [API_SECRET_KEY] 8f24613dffb00d476b4694b6814d3905e61a20a6
        os.chdir(os.path.dirname(__file__))
        try:
            accesskey = 'df34fb44-167c-47f1-a3ea-21f703231302'
            secretkey = '8f24613dffb00d476b4694b6814d3905e61a20a6'
            vendor_id = 'A00010954'
            shop_id = 'ypa0940'

            with captured_output() as (out, err):
                r = main(accesskey, secretkey,
                         vendor_id, shop_id)
            self.assertTrue(r == 0)
            _out = out.getvalue()
            print(_out)
            out.seek(0)
            self.assertTrue(_out.find('Vendor Id = "A00010954"') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_debug(self):
        # Vendor_id = A00010954,
        # accesskey = df34fb44-167c-47f1-a3ea-21f703231302
        # secretkey = 8f24613dffb00d476b4694b6814d3905e61a20a6

        # [ID] ypa0940
        # [PW] vhvhvostl77**
        # [VENDOR_ID] A00010954
        # [API_KEY] df34fb44-167c-47f1-a3ea-21f703231302
        # [SECRET_KEY] 8f24613dffb00d476b4694b6814d3905e61a20a6
        os.chdir(os.path.dirname(__file__))
        try:
            accesskey = 'df34fb44-167c-47f1-a3ea-21f703231302'
            secretkey = '8f24613dffb00d476b4694b6814d3905e61a20a6'
            vendor_id = 'A00010954'
            shop_id = 'ypa0940'

            with captured_output() as (out, err):
                r = main(accesskey, secretkey,
                         vendor_id, shop_id)
            self.assertTrue(r == 0)
            _out = out.getvalue()
            #print(_out)
            _err = err.getvalue()
            with open('A00010954-ypa0940.txt', 'w', encoding='utf-8') as ofp:
                ofp.write(_out)
            out.seek(0)
            self.assertTrue(_out.find('Vendor Id = "A00010954"') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
