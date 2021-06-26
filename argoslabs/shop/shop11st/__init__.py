"""
====================================
 :mod:`argoslabs.shop.shop11st`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Rossum API module
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/03/09]
#     - INT_KEYS에 해당되는 컬럼의 경우 비어 있으면 '0'으로 넣기
#     - CBCI_11ST_GOODS 의 PRD_NO 컬럼이름을 PRODUCT_NO로 변경
#  * [2021/03/08]
#     - ImportError: Start directory is not importable: 'argoslabs.shop.shop11st'
#  * [2021/03/05]
#     - SQL 적용
#  * [2021/03/03]
#     - starting

################################################################################
import os
import sys
import requests
import xmltodict
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
SQL_LIST = list()
INT_KEYS = (
    'exchDlvCst',       # EXCH_DLV_CST
    'rtngdDlvCst',      # RTN_GD_DLV_CST
    'selPrc',           # SEL_PRC
    'preSelPrc',        # PRE_SEL_PRC
    'dscAmtPercnt',     # DSC_AMT_PERCNT

    'addPrc',           # ADD_PRC
    'selQty',           # SEL_QTY
    'stckQty',          # STCK_QTY
    'addCompPrc',       # ADD_COMP_PRC
    'compPrdQty',       # COMP_PRD_QTY
)


################################################################################
def _v(d, k):
    if k not in d:
        return '' if k not in INT_KEYS else '0'
    v = d[k]
    if not v:
        return '' if k not in INT_KEYS else '0'

    # escape sequence for mysql
    if v.find("'") >= 0:
        v = str(v).replace("'", "''")
    if v.find("\\") >= 0:
        v = str(v).replace("\\", "\\\\")
    if v.find("\n") >= 0:
        v = str(v).replace("\n", "\\n")
    if v.find("\r") >= 0:
        v = str(v).replace("\r", "\\r")
    if v.find("\t") >= 0:
        v = str(v).replace("\t", "\\t")
    return str(v)


################################################################################
def gen_sql_goods(shop_id, pd, rd):
    sql = f'''
INSERT INTO CBCI_11ST_GOODS VALUES (
    '{shop_id}', NULL, NULL, 
    '{_v(pd, "cuponcheck")}', 
    '{_v(pd, "dispCtgrNo")}', 
    '{_v(pd, "exchDlvCst")}', 
    '{_v(pd, "prdNm")}', 
    '{_v(pd, "prdNo")}', 
    '{_v(pd, "proxyYn")}', 
    '{_v(pd, "rtngdDlvCst")}', 
    '{_v(pd, "selPrc")}', 
    '{_v(pd, "selStatCd")}', 
    '{_v(pd, "selStatNm")}', 
    '{_v(pd, "sellerPrdCd")}', 
    '{_v(pd, "prdWght")}', 
    '{_v(pd, "gblDlvYn")}', 
    '{_v(pd, "gblHsCode")}', 
    '{_v(pd, "aplBgnDy")}', 
    '{_v(pd, "aplEndDy")}', 
    '{_v(pd, "stdPrdYn")}', 
    '{_v(rd, "asDetail")}', 
    '{_v(rd, "bndlDlvCnYn")}', 
    '{_v(rd, "dispCtgrStatCd")}', 
    '{_v(rd, "outsideYnIn")}', 
    '{_v(rd, "outsideYnOut")}', 
    '{_v(rd, "dscAmtPercnt")}', 
    '{_v(rd, "cupnDscMthdCd")}', 
    '{_v(rd, "sellerItemEventYn")}', 
    '{_v(rd, "dlvClf")}', 
    '{_v(rd, "abrdCnDlvCst")}', 
    '{_v(rd, "ntNo")}', 
    '{_v(rd, "shopNo")}', 
    '{_v(rd, "ntShortNm")}', 
    '{_v(rd, "preSelPrc")}', 
    '{_v(rd, "cupnUseLmtDyYn")}', 
    '{_v(rd, "cupnIssEndDy")}', 
    '{_v(rd, "prdImage01")}', 
    DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s'), 
    DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s')
) ON DUPLICATE KEY UPDATE 
    CUPON_CHECK = '{_v(pd, "cuponcheck")}', 
    EXCH_DLV_CST = '{_v(pd, "exchDlvCst")}', 
    PRD_NM = '{_v(pd, "prdNm")}', 
    PROXY_YN = '{_v(pd, "proxyYn")}', 
    RTN_GD_DLV_CST = '{_v(pd, "rtngdDlvCst")}', 
    SEL_PRC = '{_v(pd, "selPrc")}', 
    SEL_STAT_CD = '{_v(pd, "selStatCd")}', 
    SEL_STAT_NM = '{_v(pd, "selStatNm")}', 
    SELLER_PRD_CD = '{_v(pd, "sellerPrdCd")}', 
    PRD_WGHT = '{_v(pd, "prdWght")}', 
    GBL_DLV_YN = '{_v(pd, "gblDlvYn")}', 
    GBL_HS_CODE = '{_v(pd, "gblHsCode")}', 
    APL_BGN_DAY = '{_v(pd, "aplBgnDy")}', 
    APL_END_DAY = '{_v(pd, "aplEndDy")}', 
    STD_PRD_YN = '{_v(pd, "stdPrdYn")}', 
    AS_DETAIL = '{_v(rd, "asDetail")}', 
    BNDL_DLV_CN_YN = '{_v(rd, "bndlDlvCnYn")}', 
    DISP_CTGR_STAT_CD = '{_v(rd, "dispCtgrStatCd")}', 
    OUTSIDE_YN_IN = '{_v(rd, "outsideYnIn")}', 
    OUTSIDE_YN_OUT = '{_v(rd, "outsideYnOut")}', 
    DSC_AMT_PERCNT = '{_v(rd, "dscAmtPercnt")}', 
    CUPN_DSC_MTHD_CD = '{_v(rd, "cupnDscMthdCd")}', 
    SELLER_ITEM_EVENT_YN = '{_v(rd, "sellerItemEventYn")}', 
    DLV_CLF = '{_v(rd, "dlvClf")}', 
    ABRD_CN_DLV_CST = '{_v(rd, "abrdCnDlvCst")}', 
    NT_NO = '{_v(rd, "ntNo")}', 
    SHOP_NO = '{_v(rd, "shopNo")}', 
    NT_SHORT_NM = '{_v(rd, "ntShortNm")}', 
    PRE_SEL_PRC = '{_v(rd, "preSelPrc")}', 
    CUPN_USE_LMT_DAY_YN = '{_v(rd, "cupnUseLmtDyYn")}', 
    CUPN_LSS_END_DAY = '{_v(rd, "cupnIssEndDy")}', 
    PRD_IMAGE_01 = '{_v(rd, "prdImage01")}', 
    UPD_DATE = DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s');
'''
    SQL_LIST.append(sql)


################################################################################
def gen_sql_stock(shop_id, pd, sd):
    sql = f'''
INSERT INTO CBCI_11ST_STOCK VALUES (
    '{shop_id}', NULL, NULL, 
    '{_v(pd, "prdNm")}', 
    '{_v(pd, "prdNo")}', 
    '{_v(pd, "sellerPrdCd")}', 
    '{_v(sd, "addPrc")}', 
    '{_v(sd, "mixDtlOptNm")}', 
    '{_v(sd, "mixOptNm")}', 
    '{_v(sd, "mixOptNo")}', 
    '{_v(sd, "prdStckNo")}', 
    '{_v(sd, "prdStckStatCd")}', 
    '{_v(sd, "selQty")}', 
    '{_v(sd, "stckQty")}', 
    '{_v(sd, "optWght")}', 
    '{_v(sd, "sellerStockCd")}', 
    '{_v(sd, "addCompPrc")}', 
    '{_v(sd, "addPrdGrpNm")}', 
    '{_v(sd, "addPrdWght")}', 
    '{_v(sd, "addUseYn")}', 
    '{_v(sd, "compPrdNm")}', 
    '{_v(sd, "compPrdQty")}',
    DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s'), 
    DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s')
) ON DUPLICATE KEY UPDATE 
    SELLER_PRD_CD = '{_v(pd, "sellerPrdCd")}', 
    ADD_PRC = '{_v(sd, "addPrc")}', 
    MIX_DTL_OPT_NM = '{_v(sd, "mixDtlOptNm")}', 
    MIX_OPT_NM = '{_v(sd, "mixOptNm")}', 
    MIX_OPT_NO = '{_v(sd, "mixOptNo")}', 
    PRD_STCK_STAT_CD = '{_v(sd, "prdStckStatCd")}', 
    SEL_QTY = '{_v(sd, "selQty")}', 
    STCK_QTY = '{_v(sd, "stckQty")}', 
    OPT_WGHT = '{_v(sd, "optWght")}', 
    SELLER_STOCK_CD = '{_v(sd, "sellerStockCd")}', 
    ADD_COMP_PRC = '{_v(sd, "addCompPrc")}', 
    ADD_PRD_GRP_NM = '{_v(sd, "addPrdGrpNm")}', 
    ADD_PRD_WGHT = '{_v(sd, "addPrdWght")}', 
    ADD_USE_YN = '{_v(sd, "addUseYn")}', 
    COMP_PRD_NM = '{_v(sd, "compPrdNm")}', 
    COMP_PRD_QTY = '{_v(sd, "compPrdQty")}', 
    UPD_DATE = DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s'
);
'''
    SQL_LIST.append(sql)


################################################################################
def gen_sql_category(rd):
    sql = f'''
INSERT INTO CBCI_11ST_CATEGORY VALUES ( 
    '{_v(rd, "depth")}', 
    '{_v(rd, "dispNm")}', 
    '{_v(rd, "dispNo")}', 
    '{_v(rd, "parentDispNo")}', 
    '{_v(rd, "engDispYn")}', 
    '{_v(rd, "certType")}', 
    '{_v(rd, "requiredYn")}', 
    DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s'), 
    DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s') 
) ON DUPLICATE KEY UPDATE 
    CATEGORY_DEPTH = '{_v(rd, "depth")}', 
    DISP_NM = '{_v(rd, "dispNm")}', 
    PARENT_DISP_NO = '{_v(rd, "parentDispNo")}', 
    ENG_DISP_YN = '{_v(rd, "engDispYn")}', 
    CERT_TYPE = '{_v(rd, "certType")}', 
    REQUIRED_YN = '{_v(rd, "requiredYn")}', 
    UPD_DATE = DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s'
);
'''
    SQL_LIST.append(sql)


################################################################################
def get_product_category(_key, _cno):
    headers = {
        'openapikey': _key,
        # 'Content-Type': 'text/xml',
    }
    url = f'http://api.11st.co.kr/rest/cateservice/category/{_cno}'
    resp = requests.get(url, headers=headers)
    if resp.status_code // 10 != 20:
        raise LookupError(f"Invalid API response code {resp.status_code}")
    rd = xmltodict.parse(resp.text)
    rd = rd['ns2:categorys']
    rd = rd['ns2:category']
    # print(f'{"-" * 80} Category<{_cno}>')
    # pprint.pprint(dict(rd))
    gen_sql_category(dict(rd))


################################################################################
def get_product_good(_key, shop_id, pd):
    _pno = pd['prdNo']
    headers = {
        'openapikey': _key,
        # 'Content-Type': 'text/xml',
    }
    url = f'http://api.11st.co.kr/rest/prodmarketservice/prodmarket/{_pno}'
    resp = requests.get(url, headers=headers)
    if resp.status_code // 10 != 20:
        raise LookupError(f"Invalid API response code {resp.status_code}")
    rd = xmltodict.parse(resp.text)
    rd = rd['Product']
    # print(f'{"-" * 80} Product<{_pno}>')
    # pprint.pprint(dict(rd))
    gen_sql_goods(shop_id, pd, dict(rd))


################################################################################
def get_product_stocks(_key, shop_id, pd):
    _pno = pd['prdNo']
    headers = {
        'openapikey': _key,
        'ProductStock': 'ProductStock',
        'Content-Type': 'text/xml',
    }
    xml = f"""<?xml version="1.0" encoding="euc-kr" standalone="yes"?>
    <ProductStocks>
        <ProductStock>
            <prdNo>{_pno}</prdNo>
        </ProductStock>
    </ProductStocks>
    """

    url = f'http://api.11st.co.kr/rest/prodmarketservice/prodmarket/stocks'
    resp = requests.post(url, data=xml, headers=headers)
    if resp.status_code // 10 != 20:
        raise LookupError(f"Invalid API response code {resp.status_code}")

    rd = xmltodict.parse(resp.text)
    rd = rd['ns2:ProductStockss']
    rd = rd['ns2:ProductStocks']
    rd = rd['ns2:ProductStock']
    if isinstance(rd, (list, tuple)):
        for i, st in enumerate(rd):
            # print(f'{"~" * 80} Stock <{_pno}> [{i+1} / {len(rd)}]')
            try:
                # pprint.pprint(dict(st))
                gen_sql_stock(shop_id, pd, dict(st))
            except:
                raise RuntimeError(f'get_product_stocks: Invalid stock {st}')
    else:
        # print(f'{"~" * 80} Stock <{_pno}> [{1} / {1}]')
        try:
            # pprint.pprint(dict(rd))
            gen_sql_stock(shop_id, pd, dict(rd))
        except:
            raise RuntimeError(f'get_product_stocks: Invalid stock {rd}')


################################################################################
def get_product_goods(_key, shop_id):
    headers = {
        'openapikey': _key,
        'SearchProduct': 'SearchProduct',
        'Content-Type': 'text/xml',
    }
    xml = """<?xml version="1.0" encoding="euc-kr" standalone="yes"?>
    <SearchProduct>
        <category1/>
        <category2/>
        <category3/>
        <category4/>
        <prdNo/>
        <prdNm/>
        <selStatCd/>
        <selMthdCd/>
        <schDateType/>
        <schBgnDt/>
        <schEndDt/>
        <limit>10</limit>
        <start/>
        <end/>
    </SearchProduct>
    """

    url = f'http://api.11st.co.kr/rest/prodmarketservice/prodmarket'
    resp = requests.post(url, data=xml, headers=headers)
    if resp.status_code // 10 != 20:
        raise LookupError(f"Invalid API response code {resp.status_code}")

    rd = xmltodict.parse(resp.text)
    rd = rd['ns2:products']
    rd = rd['ns2:product']

    for pd in rd:
        # print(f'\n{"="*100}')
        # pprint.pprint(dict(pd))
        dpd = dict(pd)
        get_product_good(_key, shop_id, dpd)  # pd['prdNo'])
        get_product_stocks(_key, shop_id, dpd)
        get_product_category(_key, pd['dispCtgrNo'])


################################################################################
@func_log
def do_api(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        get_product_goods(argspec.accesskey, argspec.shop_id)
        print('\n'.join(SQL_LIST))
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='api',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Shop 11st',
        icon_path=get_icon_path(__file__),
        description='11st Shopping API',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('accesskey',
                          display_name='Access key',
                          input_method='password',
                          help='Access key for 11st API')
        mcxt.add_argument('shop_id',
                          display_name='Shop Id',
                          help='Shop Id for second column')
        argspec = mcxt.parse_args(args)
        return do_api(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
