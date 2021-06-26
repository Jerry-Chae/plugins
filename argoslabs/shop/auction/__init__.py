"""
====================================
 :mod:`argoslabs.shop.auction`
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
#  * [2021/03/12]
#     - Stock의 @Type이 'NotAvailable' 이면 Insert 안함
#     - SellUnitValue의 Int 형식 추가
#  * [2021/03/10]
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
    # 상품정보 중 INT 또는 Decimal
    '@MinBuyQty',               # MinBuyQty
    '@OrderCompleteQty',        # ORDER_COMPLETE_QTY
    '@Premium',                 # PREMIUM
    '@PremiumPlus',             # PREMIUM_PLUS
    '@Recommend',               # RECOMMEND
    '@SellingPrice'             # SELLING_PRICE
    '@ShippingCondition',       # SHIPPING_CONDITION
    '@ShippingCost',            # SHIPPING_COST
    '@SumStockQty',             # SUM_STOCK_QTY

    # 재고 중 INT 또는 Decimal
    '@ItemStockStandAloneNo',   # ITEM_STOCK_STAND_ALONE_NO
    '@ObjOptClaseNo',           # OBJ_OPT_CLASE_NO
    '@Price',                   # PRICE
    '@StockMasterSeqNo',        # STOCK_MASTER_SEQ_NO
    '@StockQty',                # STOCK_QTY
    '@ItemStockCalcNo',         # ITEM_STOCK_CALC_NO
    '@MinSellAmnt',             # MIN_SELL_AMNT
    '@MinSellQty',              # MIN_SELL_QTY
    '@SellRangeMaxValue1',      # SELL_RANGE_MAX_VALUE1
    '@SellRangeMaxValue2',      # SELL_RANGE_MAX_VALUE2
    '@SellRangeMinValue1',      # SELL_RANGE_MIN_VALUE1
    '@SellRangeMinValue2',      # SELL_RANGE_MIN_VALUE2
    '@UnitPrice',               # UNIT_PRICE
    '@SellUnitValue',           # SELL_UNIT_VALUE
)


################################################################################
def _v(d, _k):
    if not isinstance(_k, (list, tuple)):
        _k = [_k]
    last_k = _k[-1]
    for i, k in enumerate(_k):
        try:
            d = d[k]
            if i > 0:
                d = d
        except:
            return '' if last_k not in INT_KEYS else '0'
    v = d
    if not v:
        return '' if last_k not in INT_KEYS else '0'

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
def gen_sql_goods(shop_id, pd):
    # ItemRegistDate, IsBundleShipping, ShippingCostChargeCode 안 보임
    sql = f'''
INSERT INTO CBCI_AUCTION_GOODS VALUES (
    '{shop_id}', NULL, NULL, 
    '{_v(pd, "@ItemNo")}', 
    '{_v(pd, "@ItemName")}', 
    '{_v(pd, "@ItemRegistDate")}', 
    '{_v(pd, "@BrandName")}', 
    '{_v(pd, "@CategoryCode")}', 
    '{_v(pd, "@CategoryName")}', 
    '{_v(pd, "@FreeGift")}', 
    '{_v(pd, "@IsArrival")}', 
    '{_v(pd, "@IsBundleShipping")}', 
    '{_v(pd, "@IsShippingPrePayable")}', 
    '{_v(pd, "@ListingBeginDate")}', 
    '{_v(pd, "@ListingEndDate")}', 
    '{_v(pd, "@ManagementCode")}', 
    '{_v(pd, "@MinBuyQty")}', 
    '{_v(pd, "@ModelName")}', 
    '{_v(pd, "@OptionTypeCode")}', 
    '{_v(pd, "@OrderCompleteQty")}', 
    '{_v(pd, "@OrderTypeCode")}', 
    '{_v(pd, "@Premium")}', 
    '{_v(pd, "@PremiumPlus")}', 
    '{_v(pd, "@Recommend")}', 
    '{_v(pd, "@SellingPrice")}', 
    '{_v(pd, "@SellingStatusCode")}', 
    '{_v(pd, "@ShippingCondition")}', 
    '{_v(pd, "@ShippingCost")}', 
    '{_v(pd, "@ShippingCostChargeCode")}', 
    '{_v(pd, "@ShippingFeeChargeType")}', 
    '{_v(pd, "@ShippingFeeType")}', 
    '{_v(pd, "@SumStockQty")}', 
    DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s'), 
    DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s')
) ON DUPLICATE KEY 
    UPDATE ITEM_NAME = '{_v(pd, "@ItemName")}', 
    ITEM_REGIST_DATE = '{_v(pd, "@ItemRegistDate")}', 
    BRAND_NAME = '{_v(pd, "@BrandName")}', 
    CATEGORY_CODE = '{_v(pd, "@CategoryCode")}', 
    CATEGORY_NAME = '{_v(pd, "@CategoryName")}', 
    FREE_GIFT = '{_v(pd, "@FreeGift")}', 
    IS_ARRIVAL = '{_v(pd, "@IsArrival")}', 
    IS_BUNDLE_SHIPPING = '{_v(pd, "@IsBundleShipping")}', 
    IS_SHIPPING_PRE_PAYABLE = '{_v(pd, "@IsShippingPrePayable")}', 
    LISTING_BEGIN_DATE = '{_v(pd, "@ListingBeginDate")}', 
    LISTING_END_DATE = '{_v(pd, "@ListingEndDate")}', 
    MANAGEMENT_CODE = '{_v(pd, "@ManagementCode")}', 
    MIN_BUY_QTY = '{_v(pd, "@MinBuyQty")}', 
    MODEL_NAME = '{_v(pd, "@ModelName")}', 
    OPTION_TYPE_CODE = '{_v(pd, "@OptionTypeCode")}', 
    ORDER_COMPLETE_QTY = '{_v(pd, "@OrderCompleteQty")}', 
    ORDER_TYPE_CODE = '{_v(pd, "@OrderTypeCode")}', 
    PREMIUM = '{_v(pd, "@Premium")}', 
    PREMIUM_PLUS = '{_v(pd, "@PremiumPlus")}', 
    RECOMMEND = '{_v(pd, "@Recommend")}', 
    SELLING_PRICE = '{_v(pd, "@SellingPrice")}', 
    SELLING_STATUS_CODE = '{_v(pd, "@SellingStatusCode")}', 
    SHIPPING_CONDITION = '{_v(pd, "@ShippingCondition")}', 
    SHIPPING_COST = '{_v(pd, "@ShippingCost")}', 
    SHIPPING_COST_CHARGE_CODE = '{_v(pd, "@ShippingCostChargeCode")}', 
    SHIPPING_FEE_CHARGE_TYPE = '{_v(pd, "@ShippingFeeChargeType")}', 
    SHIPPING_FEE_TYPE = '{_v(pd, "@ShippingFeeType")}', 
    SUM_STOCK_QTY = '{_v(pd, "@SumStockQty")}', 
    UPD_DATE = DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s'
);
'''
    SQL_LIST.append(sql)


################################################################################
def gen_sql_stock(shop_id, pd, sd):
    # StockStandAlone 의 목록 항목에서 반복되는 것:
    #   ItemStockStandAloneNo, IsSoldOut, ObjOptClaseNo, Price, Section,
    #   SellerStockCode, StockMasterSeqNo, StockQty, Text, UseYN
    # OptionObjectName 에서 반복되는
    #   ClaseName1 은 첫번째 것만
    # ItemStockCalcNo, ChangeType, ImageUrl, ClaseName2, MinSellAmnt, MinSellQty,
    # SellRangeMaxValue1, SellRangeMaxValue2, SellRangeMinValue1, SellRangeMinValue2,
    # SellUnitType, SellUnitValue, UnitPrice 안 보임
    if _v(sd, "@Type") == 'NotAvailable':
        return False
    ssa_len = len(sd.get('StockStandAlone', []))
    if ssa_len <= 0:
        ssa_ndx = 0
        sql = f'''
INSERT INTO CBCI_AUCTION_STOCK VALUES (
    '{shop_id}', NULL, NULL, 
    '{_v(pd, "@ItemNo")}', 
    '{_v(sd, "@Type")}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@ItemStockStandAloneNo"])}', 
    '{_v(sd, "@ItemStockCalcNo")}', 
    '{_v(sd, "@IsStockQtyMng")}', 
    '{_v(sd, "@OptionStockType")}', 
    '{_v(sd, "@OptVerType")}', 
    '{_v(sd, "@ChangeType")}', 
    '{_v(sd, "@ImageUrl")}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@IsSoldOut"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@ObjOptClaseNo"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@Price"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@Section"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@SellerStockCode"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@StockMasterSeqNo"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@StockQty"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@Text"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@UseYN"])}', 
    '{_v(sd, ["OptionObjectName", 0, "@ClaseName1"])}', 
    '{_v(sd, ["OptionObjectName", 0, "@ClaseName2"])}', 
    '{_v(sd, "@MinSellAmnt")}', 
    '{_v(sd, "@MinSellQty")}', 
    '{_v(sd, "@SellRangeMaxValue1")}', 
    '{_v(sd, "@SellRangeMaxValue2")}', 
    '{_v(sd, "@SellRangeMinValue1")}', 
    '{_v(sd, "@SellRangeMinValue2")}', 
    '{_v(sd, "@SellUnitType")}', 
    '{_v(sd, "@SellUnitValue")}', 
    '{_v(sd, "@UnitPrice")}', 
    DATE_FORMAT(now(),'%Y-%m-%d %H:%i:%s'), 
    DATE_FORMAT(now(),'%Y-%m-%d %H:%i:%s')
) ON DUPLICATE KEY UPDATE 
    STOCK_TYPE = '{_v(sd, "@Type")}', 
    IS_STOCK_QTY_MNG = '{_v(sd, "@IsStockQtyMng")}', 
    OPTION_STOCK_TYPE = '{_v(sd, "@OptionStockType")}', 
    OPT_VER_TYPE = '{_v(sd, "@OptVerType")}', 
    CHANGE_TYPE = '{_v(sd, "@ChangeType")}', 
    IMAGE_URL = '{_v(sd, "@ImageUrl")}', 
    IS_SOLD_OUT = '{_v(sd, ["StockStandAlone", ssa_ndx, "@IsSoldOut"])}', 
    OBJ_OPT_CLASE_NO = '{_v(sd, ["StockStandAlone", ssa_ndx, "@ObjOptClaseNo"])}', 
    PRICE = '{_v(sd, ["StockStandAlone", ssa_ndx, "@Price"])}', 
    ALONE_SECTION = '{_v(sd, ["StockStandAlone", ssa_ndx, "@Section"])}', 
    SELLER_STOCK_CODE = '{_v(sd, ["StockStandAlone", ssa_ndx, "@SellerStockCode"])}', 
    STOCK_MASTER_SEQ_NO = '{_v(sd, ["StockStandAlone", ssa_ndx, "@StockMasterSeqNo"])}', 
    STOCK_QTY = '{_v(sd, ["StockStandAlone", ssa_ndx, "@StockQty"])}', 
    ALONE_TEXT = '{_v(sd, ["StockStandAlone", ssa_ndx, "@Text"])}', 
    USE_YN = '{_v(sd, ["StockStandAlone", ssa_ndx, "@UseYN"])}', 
    CLASS_NAME1 = '{_v(sd, ["OptionObjectName", 0, "@ClaseName1"])}', 
    CLASS_NAME2 = '{_v(sd, ["OptionObjectName", 0, "@ClaseName2"])}', 
    MIN_SELL_AMNT = '{_v(sd, "@MinSellAmnt")}', 
    MIN_SELL_QTY = '{_v(sd, "@MinSellQty")}', 
    SELL_RANGE_MAX_VALUE1 = '{_v(sd, "@SellRangeMaxValue1")}', 
    SELL_RANGE_MAX_VALUE2 = '{_v(sd, "@SellRangeMaxValue2")}', 
    SELL_RANGE_MIN_VALUE1 = '{_v(sd, "@SellRangeMinValue1")}', 
    SELL_RANGE_MIN_VALUE2 = '{_v(sd, "@SellRangeMinValue2")}', 
    SELL_UNIT_TYPE = '{_v(sd, "@SellUnitType")}', 
    SELL_UNIT_VALUE = '{_v(sd, "@SellUnitValue")}', 
    UNIT_PRICE = '{_v(sd, "@UnitPrice")}', 
    UPD_DATE = DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s'
);
'''
        SQL_LIST.append(sql)
    for ssa_ndx in range(ssa_len):
        sql = f'''
INSERT INTO CBCI_AUCTION_STOCK VALUES (
    '{shop_id}', NULL, NULL, 
    '{_v(pd, "@ItemNo")}', 
    '{_v(sd, "@Type")}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@ItemStockStandAloneNo"])}', 
    '{_v(sd, "@ItemStockCalcNo")}', 
    '{_v(sd, "@IsStockQtyMng")}', 
    '{_v(sd, "@OptionStockType")}', 
    '{_v(sd, "@OptVerType")}', 
    '{_v(sd, "@ChangeType")}', 
    '{_v(sd, "@ImageUrl")}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@IsSoldOut"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@ObjOptClaseNo"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@Price"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@Section"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@SellerStockCode"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@StockMasterSeqNo"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@StockQty"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@Text"])}', 
    '{_v(sd, ["StockStandAlone", ssa_ndx, "@UseYN"])}', 
    '{_v(sd, ["OptionObjectName", 0, "@ClaseName1"])}', 
    '{_v(sd, ["OptionObjectName", 0, "@ClaseName2"])}', 
    '{_v(sd, "@MinSellAmnt")}', 
    '{_v(sd, "@MinSellQty")}', 
    '{_v(sd, "@SellRangeMaxValue1")}', 
    '{_v(sd, "@SellRangeMaxValue2")}', 
    '{_v(sd, "@SellRangeMinValue1")}', 
    '{_v(sd, "@SellRangeMinValue2")}', 
    '{_v(sd, "@SellUnitType")}', 
    '{_v(sd, "@SellUnitValue")}', 
    '{_v(sd, "@UnitPrice")}', 
    DATE_FORMAT(now(),'%Y-%m-%d %H:%i:%s'), 
    DATE_FORMAT(now(),'%Y-%m-%d %H:%i:%s')
) ON DUPLICATE KEY UPDATE 
    STOCK_TYPE = '{_v(sd, "@Type")}', 
    IS_STOCK_QTY_MNG = '{_v(sd, "@IsStockQtyMng")}', 
    OPTION_STOCK_TYPE = '{_v(sd, "@OptionStockType")}', 
    OPT_VER_TYPE = '{_v(sd, "@OptVerType")}', 
    CHANGE_TYPE = '{_v(sd, "@ChangeType")}', 
    IMAGE_URL = '{_v(sd, "@ImageUrl")}', 
    IS_SOLD_OUT = '{_v(sd, ["StockStandAlone", ssa_ndx, "@IsSoldOut"])}', 
    OBJ_OPT_CLASE_NO = '{_v(sd, ["StockStandAlone", ssa_ndx, "@ObjOptClaseNo"])}', 
    PRICE = '{_v(sd, ["StockStandAlone", ssa_ndx, "@Price"])}', 
    ALONE_SECTION = '{_v(sd, ["StockStandAlone", ssa_ndx, "@Section"])}', 
    SELLER_STOCK_CODE = '{_v(sd, ["StockStandAlone", ssa_ndx, "@SellerStockCode"])}', 
    STOCK_MASTER_SEQ_NO = '{_v(sd, ["StockStandAlone", ssa_ndx, "@StockMasterSeqNo"])}', 
    STOCK_QTY = '{_v(sd, ["StockStandAlone", ssa_ndx, "@StockQty"])}', 
    ALONE_TEXT = '{_v(sd, ["StockStandAlone", ssa_ndx, "@Text"])}', 
    USE_YN = '{_v(sd, ["StockStandAlone", ssa_ndx, "@UseYN"])}', 
    CLASS_NAME1 = '{_v(sd, ["OptionObjectName", 0, "@ClaseName1"])}', 
    CLASS_NAME2 = '{_v(sd, ["OptionObjectName", 0, "@ClaseName2"])}', 
    MIN_SELL_AMNT = '{_v(sd, "@MinSellAmnt")}', 
    MIN_SELL_QTY = '{_v(sd, "@MinSellQty")}', 
    SELL_RANGE_MAX_VALUE1 = '{_v(sd, "@SellRangeMaxValue1")}', 
    SELL_RANGE_MAX_VALUE2 = '{_v(sd, "@SellRangeMaxValue2")}', 
    SELL_RANGE_MIN_VALUE1 = '{_v(sd, "@SellRangeMinValue1")}', 
    SELL_RANGE_MIN_VALUE2 = '{_v(sd, "@SellRangeMinValue2")}', 
    SELL_UNIT_TYPE = '{_v(sd, "@SellUnitType")}', 
    SELL_UNIT_VALUE = '{_v(sd, "@SellUnitValue")}', 
    UNIT_PRICE = '{_v(sd, "@UnitPrice")}', 
    UPD_DATE = DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s'
);
'''
        SQL_LIST.append(sql)
    return True


################################################################################
def get_product_stocks(_key, shop_id, pd):
    item_id = pd['@ItemNo']
    headers = {'content-type': 'text/xml'}
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Header>
        <EncryptedTicket xmlns="http://www.auction.co.kr/Security">
    <Value>{_key}</Value>
        </EncryptedTicket>
      </soap:Header>
      <soap:Body>
    <ViewItemStock xmlns = "http://www.auction.co.kr/APIv1/ShoppingService">
          <req ItemID = "{item_id}" Version = "1">
          </req>
        </ViewItemStock>
    </soap:Body>
    </soap:Envelope>"""

    # url = f'http://api.auction.co.kr/APIv1/AuctionService.asmx'
    url = f'http://api.auction.co.kr/APIv1/ShoppingService.asmx?WSDL'
    resp = requests.post(url, data=xml, headers=headers)
    if resp.status_code // 10 != 20:
        raise LookupError(f"Invalid API response code {resp.status_code}")

    # print(resp.text)
    rd = xmltodict.parse(resp.text)
    # pprint.pprint(rd)
    rd = rd['soap:Envelope']['soap:Body']['ViewItemStockResponse'] \
        ['ViewItemStockResult']['ItemStock']
    sd = dict(rd)
    # print(f'Stock[{item_id}]{"-" * 80}')
    # pprint.pprint(rd)
    gen_sql_stock(shop_id, pd, sd)


################################################################################
def get_product_goods(_key, shop_id):
    headers = {'content-type': 'text/xml'}
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Header>
        <EncryptedTicket xmlns="http://www.auction.co.kr/Security">
            <Value>{_key}</Value>
        </EncryptedTicket>
      </soap:Header>
      <soap:Body>
        <GetSellingItemList xmlns="http://www.auction.co.kr/APIv1/ShoppingService">
          <req Version="1">
            <SearchCondition xmlns="http://schema.auction.co.kr/Arche.Sell3.Service.xsd" />
          </req>
        </GetSellingItemList>
      </soap:Body>
    </soap:Envelope>"""

    # url = f'http://api.auction.co.kr/APIv1/AuctionService.asmx'
    url = f'http://api.auction.co.kr/APIv1/ShoppingService.asmx?WSDL'
    resp = requests.post(url, data=xml, headers=headers)
    if resp.status_code // 10 != 20:
        raise LookupError(f"Invalid API response code {resp.status_code}")

    # print(resp.text)
    rd = xmltodict.parse(resp.text)
    # pprint.pprint(rd)
    rd = rd['soap:Envelope']['soap:Body']['GetSellingItemListResponse'] \
        ['GetSellingItemListResult']['SearchResult']['ItemList']
    if isinstance(rd, (list, tuple)):
        for gd in rd:
            gd = dict(gd)
            # print(f'Goods{"=" * 80}')
            # pprint.pprint(gd)
            gen_sql_goods(shop_id, gd)
            get_product_stocks(_key, shop_id, gd)
    else:
        gd = dict(rd)
        # print(f'Goods{"=" * 80}')
        # pprint.pprint(gd)
        gen_sql_goods(shop_id, gd)
        get_product_stocks(_key, shop_id, gd['@ItemNo'])


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
        display_name='Shop Auction',
        icon_path=get_icon_path(__file__),
        description='Auction Shopping API',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('accesskey',
                          display_name='Auth key',
                          input_method='password',
                          help='Authentication API key for Auction API')
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
