"""
====================================
 :mod:`argoslabs.api.coupang`
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
import json
import hmac
import base64
import hashlib
import requests
import datetime
import dpath.util
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
# from pprint import pprint
from io import StringIO


################################################################################
OPS = [
    {
        'name': '01 - 상품 조회 API > 상품 목록 페이징 조회',
        'header': ('sellerProductId', 'sellerProductName', 'displayCategoryCode',
                   'categoryId', 'productId', 'vendorId', 'saleStartedAt',
                   'saleEndedAt', 'brand', 'statusName', 'createdAt'),
    },
    {
        'name': '02 - 상품 조회 API > 상품조회',
        'header': (
            'displayProductName', 'generalProductName', 'productGroup',
            'deliveryMethod', 'deliveryCompanyCode', 'deliveryChargeType',
            'deliveryCharge', 'freeShipOverAmount', 'deliveryChargeOnReturn',
            'remoteAreaDeliverable', 'unionDeliveryType', 'returnCenterCode',
            'returnChargeName', 'companyContactNumber', 'returnZipCode',
            'returnAddress', 'returnAddressDetail', 'returnCharge',
            'returnChargeVendor', 'afterServiceInformation', 'afterServiceContactNumber',
            'outboundShippingPlaceCode', 'vendorUserId',
            'requested', 'extraInfoMessage',  'manufacture'
        ),
    },
    {
        'name': '03 - 재고관리 API > 상품조회',
        'header': (
            'sellerProductId', 'sellerProductItemId', 'vendorItemId',
            'itemName', 'originalPrice', 'salePrice',
            'maximumBuyCount', 'maximumBuyForPerson', 'maximumBuyForPersonPeriod',
            'outboundShippingTimeDay', 'adultOnly', 'taxType',
            'parallelImported', 'overseasPurchased', 'pccNeeded',
            'bestPriceGuaranteed3P', 'externalVendorSku', 'barcode',
            'emptyBarcode', 'emptyBarcodeReason', 'modelNo',
            'extraProperties', 'offerCondition', 'offerDescription',
            'certificationType', 'certificationCode',
            'imageOrder', 'imageType', 'cdnPath', 'vendorPath',
            'noticeCategoryName_1', 'noticeCategoryDetailName_1', 'content_1',
            'noticeCategoryName_2', 'noticeCategoryDetailName_2', 'content_2',
            'noticeCategoryName_3', 'noticeCategoryDetailName_3', 'content_3',
            'noticeCategoryName_4', 'noticeCategoryDetailName_4', 'content_4',
            'noticeCategoryName_5', 'noticeCategoryDetailName_5', 'content_5',
            'noticeCategoryName_6', 'noticeCategoryDetailName_6', 'content_6',
            'noticeCategoryName_7', 'noticeCategoryDetailName_7', 'content_7',
            'noticeCategoryName_8', 'noticeCategoryDetailName_8', 'content_8',
            'noticeCategoryName_9', 'noticeCategoryDetailName_9', 'content_9',
            'noticeCategoryName_10', 'noticeCategoryDetailName_10', 'content_10',
            'noticeCategoryName_11', 'noticeCategoryDetailName_10', 'content_11',
            'noticeCategoryName_12', 'noticeCategoryDetailName_10', 'content_12',
            'noticeCategoryName_13', 'noticeCategoryDetailName_10', 'content_13',
            'noticeCategoryName_14', 'noticeCategoryDetailName_10', 'content_14',
            'noticeCategoryName_15', 'noticeCategoryDetailName_10', 'content_15',
            'noticeCategoryName_16', 'noticeCategoryDetailName_10', 'content_16',
            'attributeTypeName_1', 'attributeValueName_1', 'exposed_1', 'editable_1',
            'attributeTypeName_2', 'attributeValueName_2', 'exposed_2', 'editable_2',
            'attributeTypeName_3', 'attributeValueName_3', 'exposed_3', 'editable_3',
            "contentsType_1", 'contentsDTContent_1', 'contentsDTType_1',
            "contentsType_2", 'contentsDTContent_2', 'contentsDTType_2',
            "contentsType_3", 'contentsDTContent_3', 'contentsDTType_3',
            "contentsType_4", 'contentsDTContent_4', 'contentsDTType_4',
            "contentsType_5", 'contentsDTContent_5', 'contentsDTType_5',
        ),
    },
    {
        'name': '04 - 재고관리 API > 상품 아이템별 수량/가격/상태 조회',
        'header': ('sellerItemId', 'amountInStock', 'salePrice', 'onSale'),
    },
    {
        'name': '05 - 카테고리 API > 카테고리 조회',
        'header': ('displayItemCategoryCode', 'name', 'status', 'child'),
    },
]

SQL_CBCI_COUPANG_STOCK = '''INSERT INTO CBCI_COUPANG_STOCK VALUES ('SHOP_ID', NULL, NULL, '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}', '{20}', '{21}', '{22}', '{23}', '{24}', '{25}', '{26}', '{27}', '{28}', '{29}', '{30}', '{31}', '{32}', '{33}', '{34}', '{35}', '{36}', '{37}', '{38}', '{39}', '{40}', '{41}', '{42}', '{43}', '{44}', '{45}', '{46}', '{47}', '{48}', '{49}', '{50}', '{51}', '{52}', '{53}', '{54}', '{55}', '{56}', '{57}', '{58}', '{59}', '{60}', '{61}', '{62}', '{63}', '{64}', '{65}', '{66}', '{67}', '{68}', '{69}', '{70}', '{71}', '{72}', '{73}', '{74}', '{75}', '{76}', '{77}', '{78}', '{79}', '{80}', '{81}', '{82}', '{83}', '{84}', '{85}', '{86}', '{87}', '{88}', '{89}', '{90}', '{91}', '{92}', '{93}', '{94}', '{95}', '{96}', '{97}', '{98}', '{99}', '{100}', '{101}', '{102}', '{103}', '{104}', '{105}', '{106}', '{107}', '{108}', DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s'), DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s')) ON DUPLICATE KEY UPDATE ITEM_NAME = '{3}', ORIGINAL_PRICE = '{4}', SALE_PRICE = '{5}', MAX_BUY_COUNT = '{6}', MAX_BUY_FOR_PERSON = '{7}', MAX_BUY_FOR_PERSON_PERIOD = '{8}', OUTBOUND_SHIP_TIME = '{9}', ADULT_ONLY = '{10}', TAX_TYPE = '{11}', PARALLEL_IMPORT = '{12}', OVERSEA_PURCHASED = '{13}', PCC_NEED = '{14}', BEST_PRICE_GUARANTEE = '{15}', EXTERNAL_VENDOR_SKU = '{16}', BARCODE = '{17}', BARCODE_EMPTY = '{18}', BARCODE_EMPTY_REASON = '{19}', MODEL_NO = '{20}', EXTRA_PROPERTIES = '{21}', OFFER_CONDITION = '{22}', OFFER_DESCRIPTION = '{23}', CERTIFI_TYPE_1 = '{24}', CERTIFI_CODE_1 = '{25}', IMAGE_ORDER_1 = '{26}', IMAGE_TYPE_1 = '{27}', CDN_PATH_1 = '{28}', VENDOR_PATH_1 = '{29}', NOTICE_CATEGORY_NM_1 = '{30}', NOTICE_CATEGORY_DT_NM_1 = '{31}', NOTICE_CONTENT_1 = '{32}', NOTICE_CATEGORY_NM_2 = '{33}', NOTICE_CATEGORY_DT_NM_2 = '{34}', NOTICE_CONTENT_2 = '{35}', NOTICE_CATEGORY_NM_3 = '{36}', NOTICE_CATEGORY_DT_NM_3 = '{37}', NOTICE_CONTENT_3 = '{38}', NOTICE_CATEGORY_NM_4 = '{39}', NOTICE_CATEGORY_DT_NM_4 = '{40}', NOTICE_CONTENT_4 = '{41}', NOTICE_CATEGORY_NM_5 = '{42}', NOTICE_CATEGORY_DT_NM_5 = '{43}', NOTICE_CONTENT_5 = '{44}', NOTICE_CATEGORY_NM_6 = '{45}', NOTICE_CATEGORY_DT_NM_6 = '{46}', NOTICE_CONTENT_6 = '{47}', NOTICE_CATEGORY_NM_7 = '{48}', NOTICE_CATEGORY_DT_NM_7 = '{49}', NOTICE_CONTENT_7 = '{50}', NOTICE_CATEGORY_NM_8 = '{51}', NOTICE_CATEGORY_DT_NM_8 = '{52}', NOTICE_CONTENT_8 = '{53}', NOTICE_CATEGORY_NM_9 = '{54}', NOTICE_CATEGORY_DT_NM_9 = '{55}', NOTICE_CONTENT_9 = '{56}', NOTICE_CATEGORY_NM_10 = '{57}', NOTICE_CATEGORY_DT_NM_10 = '{58}', NOTICE_CONTENT_10 = '{59}', NOTICE_CATEGORY_NM_11 = '{60}', NOTICE_CATEGORY_DT_NM_11 = '{61}', NOTICE_CONTENT_11 = '{62}', NOTICE_CATEGORY_NM_12 = '{63}', NOTICE_CATEGORY_DT_NM_12 = '{64}', NOTICE_CONTENT_12 = '{65}', NOTICE_CATEGORY_NM_13 = '{66}', NOTICE_CATEGORY_DT_NM_13 = '{67}', NOTICE_CONTENT_13 = '{68}', NOTICE_CATEGORY_NM_14 = '{69}', NOTICE_CATEGORY_DT_NM_14 = '{70}', NOTICE_CONTENT_14 = '{71}', NOTICE_CATEGORY_NM_15 = '{72}', NOTICE_CATEGORY_DT_NM_15 = '{73}', NOTICE_CONTENT_15 = '{74}', NOTICE_CATEGORY_NM_16 = '{75}', NOTICE_CATEGORY_DT_NM_16 = '{76}', NOTICE_CONTENT_16 = '{77}', ATTRIBUTE_TYPE_NAME_1 = '{78}', ATTRIBUTE_VALUE_NAME_1 = '{79}', EXPOSED_1 = '{80}', EDITABlE_1 = '{81}', ATTRIBUTE_TYPE_NAME_2 = '{82}', ATTRIBUTE_VALUE_NAME_2 = '{83}', EXPOSED_2 = '{84}', EDITABlE_2 = '{85}', ATTRIBUTE_TYPE_NAME_3 = '{86}', ATTRIBUTE_VALUE_NAME_3 = '{87}', EXPOSED_3 = '{88}', EDITABlE_3 = '{89}', CONTENTS_TYPE_1 = '{90}', CONTENTS_DT_1_CONTENT_1 = '{91}', CONTENTS_DT_1_DT_TYPE_1 = '{92}', CONTENTS_TYPE_2 = '{93}', CONTENTS_DT_1_CONTENT_2 = '{94}', CONTENTS_DT_1_DT_TYPE_2 = '{95}', CONTENTS_TYPE_3 = '{96}', CONTENTS_DT_1_CONTENT_3 = '{97}', CONTENTS_DT_1_DT_TYPE_3 = '{98}', CONTENTS_TYPE_4 = '{99}', CONTENTS_DT_1_CONTENT_4 = '{100}', CONTENTS_DT_1_DT_TYPE_4 = '{101}', CONTENTS_TYPE_5 = '{102}', CONTENTS_DT_1_CONTENT_5 = '{103}', CONTENTS_DT_1_DT_TYPE_5 = '{104}', OPT_SELLER_ITEM_ID = '{105}', OPT_AMOUNT_IN_STOCK = '{106}', OPT_SALE_PRICE = '{107}', OPT_ON_SALE = '{108}', UPD_DATE = DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s');'''


################################################################################
def get_op_names():
    op_names = []
    for op in OPS:
        op_names.append(op['name'])
    return op_names


################################################################################
def seller_products_01(accesskey, secretkey, vendor_id, sio,
                       seller_product_ids, display_category_codes):
    _datetime = datetime.datetime.utcnow().strftime('%y%m%dT%H%M%SZ')
    method = "GET"
    path = '/v2/providers/seller_api/apis/api/v1/marketplace/seller-products'
    query = f'vendorId={vendor_id}'
    message = _datetime + method + path + query
    url = "https://api-gateway.coupang.com" + path + '?' + query
    signature = hmac.new(secretkey.encode('utf-8'), message.encode('utf-8'),
                         hashlib.sha256).hexdigest()
    authorization = "CEA algorithm=HmacSHA256, access-key=" + accesskey + \
                    ", signed-date=" + _datetime + ", signature=" + signature
    headers = {
        'Content-type': 'application/json;charset=UTF-8',
        'Authorization': authorization,
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code // 10 != 20:
        # sys.stderr.write(resp.text)
        raise LookupError(f"seller_products_01: Invalid API response {resp.status_code}:{resp.text}")
    rj = json.loads(resp.text)
    # sio.write(f'--- {OPS[0]["name"]} : {len(rj["data"])} records\n')
    rows = list()
    for dj in rj['data']:
        row = list()
        for h in OPS[0]['header']:
            if h in dj:
                row.append(dj[h])
            else:
                row.append('')
                raise ReferenceError(f'Op 01: Invalid key "{h}"')
        seller_product_ids.append(row[0])
        display_category_codes.append(row[2])
        rows.append(row)
    return rows


################################################################################
def get_product_02(accesskey, secretkey, seller_product_id):
    # c.writerow(OPS[1]['header'])
    _datetime = datetime.datetime.utcnow().strftime('%y%m%dT%H%M%SZ')
    method = "GET"
    path = f'/v2/providers/seller_api/apis/api/v1/marketplace/seller-products/{seller_product_id}'
    message = _datetime + method + path
    url = "https://api-gateway.coupang.com" + path
    signature = hmac.new(secretkey.encode('utf-8'), message.encode('utf-8'),
                         hashlib.sha256).hexdigest()
    authorization = "CEA algorithm=HmacSHA256, access-key=" + accesskey + \
                    ", signed-date=" + _datetime + ", signature=" + signature
    headers = {
        'Content-type': 'application/json;charset=UTF-8',
        'Authorization': authorization,
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code // 10 != 20:
        # sys.stderr.write(resp.text)
        raise LookupError(f"get_product_02: Invalid API response {resp.status_code}:{resp.text}")
    # print(resp.text)
    rj = json.loads(resp.text)
    dj = rj['data']
    # pprint(dj)
    row = list()
    for h in OPS[1]['header']:
        if h in dj:
            row.append(dj[h])
        else:
            row.append('')
            raise ReferenceError(f'Op 02: Invalid key "{h}"')
    # c.writerow(row)
    return row


################################################################################
def get_representation_iamge(imgs):
    for img in imgs:
        if [img.get('imageType') == 'REPRESENTATION']:
            return img
    return None


################################################################################
def get_product_03(accesskey, secretkey, seller_product_id, vendor_item_ids):
    # c.writerow(OPS[2]['header'])
    _datetime = datetime.datetime.utcnow().strftime('%y%m%dT%H%M%SZ')
    method = "GET"
    path = f'/v2/providers/seller_api/apis/api/v1/marketplace/seller-products/{seller_product_id}'
    message = _datetime + method + path
    url = "https://api-gateway.coupang.com" + path
    signature = hmac.new(secretkey.encode('utf-8'), message.encode('utf-8'),
                         hashlib.sha256).hexdigest()
    authorization = "CEA algorithm=HmacSHA256, access-key=" + accesskey + \
                    ", signed-date=" + _datetime + ", signature=" + signature
    headers = {
        'Content-type': 'application/json;charset=UTF-8',
        'Authorization': authorization,
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code // 10 != 20:
        # sys.stderr.write(resp.text)
        raise LookupError(f"get_product_03: Invalid API response {resp.status_code}:{resp.text}")
    # print(resp.text)
    rj = json.loads(resp.text)
    rows = list()
    for dj in rj['data']['items']:
        # pprint(dj)
        row = list()
        rep_image = get_representation_iamge(dj.get('images', []))
        for h in OPS[2]['header']:
            if h == 'sellerProductId':
                row.append(seller_product_id)
            elif h == 'certificationCode':
                row.append(dpath.util.get(dj, '/certifications/01/certificationCode', default=''))
            elif h == 'certificationType':
                row.append(dpath.util.get(dj, '/certifications/01/certificationType', default=''))
            elif h == 'imageOrder' and rep_image:
                row.append(dpath.util.get(rep_image, '/imageOrder', default=''))
            elif h == 'imageType' and rep_image:
                row.append(dpath.util.get(rep_image, '/imageType', default=''))
            elif h == 'cdnPath' and rep_image:
                row.append(dpath.util.get(rep_image, '/cdnPath', default=''))
            elif h == 'vendorPath' and rep_image:
                row.append(dpath.util.get(rep_image, '/vendorPath', default=''))
            elif h.startswith('noticeCategoryName_'):
                ndx = int(h.split('_')[1]) - 1
                row.append(dpath.util.get(dj, f'/notices/{ndx}/noticeCategoryName', default=''))
            elif h.startswith('noticeCategoryDetailName_'):
                ndx = int(h.split('_')[1]) - 1
                row.append(dpath.util.get(dj, f'/notices/{ndx}/noticeCategoryDetailName', default=''))
            elif h.startswith('content_'):
                ndx = int(h.split('_')[1]) - 1
                row.append(dpath.util.get(dj, f'/notices/{ndx}/content', default=''))
            elif h.startswith('attributeTypeName_'):
                ndx = int(h.split('_')[1]) - 1
                row.append(dpath.util.get(dj, f'/attributes/{ndx}/attributeTypeName', default=''))
            elif h.startswith('attributeValueName_'):
                ndx = int(h.split('_')[1]) - 1
                row.append(dpath.util.get(dj, f'/attributes/{ndx}/attributeValueName', default=''))
            elif h.startswith('exposed_'):
                ndx = int(h.split('_')[1]) - 1
                row.append(dpath.util.get(dj, f'/attributes/{ndx}/exposed', default=''))
            elif h.startswith('editable_'):
                ndx = int(h.split('_')[1]) - 1
                row.append(dpath.util.get(dj, f'/attributes/{ndx}/editable', default=''))
            elif h.startswith('contentsType_'):
                ndx = int(h.split('_')[1]) - 1
                row.append(dpath.util.get(dj, f'/contents/{ndx}/contentsType', default=''))
            elif h.startswith('contentsDTContent_'):
                ndx = int(h.split('_')[1]) - 1
                row.append(dpath.util.get(dj, f'/contents/{ndx}/contentDetails/0/content', default=''))
            elif h.startswith('contentsDTType_'):
                ndx = int(h.split('_')[1]) - 1
                row.append(dpath.util.get(dj, f'/contents/{ndx}/contentDetails/0/detailType', default=''))
            else:
                if h in dj:
                    row.append(dj[h])
                    # if h == 'externalVendorSku':  # index 16
                    #     h = h
                else:
                    row.append('')
                    raise ReferenceError(f'Op 03: Invalid key "{h}"')
        # c.writerow(row)
        vendor_item_ids.append(row[2])
        rows.append(row)
    return rows


################################################################################
def get_inventories_04(accesskey, secretkey, vender_item_id):
    # c.writerow(OPS[3]['header'])
    _datetime = datetime.datetime.utcnow().strftime('%y%m%dT%H%M%SZ')
    method = "GET"
    path = f'/v2/providers/seller_api/apis/api/v1/marketplace/vendor-items/{vender_item_id}/inventories'
    message = _datetime + method + path
    url = "https://api-gateway.coupang.com" + path
    signature = hmac.new(secretkey.encode('utf-8'), message.encode('utf-8'),
                         hashlib.sha256).hexdigest()
    authorization = "CEA algorithm=HmacSHA256, access-key=" + accesskey + \
                    ", signed-date=" + _datetime + ", signature=" + signature
    headers = {
        'Content-type': 'application/json;charset=UTF-8',
        'Authorization': authorization,
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code // 10 != 20:
        sys.stderr.write(resp.text)
        raise LookupError(f"get_product_02: Invalid API response code {resp.status_code}")
    # print(resp.text)
    rj = json.loads(resp.text)
    dj = rj['data']
    # pprint(dj)
    row = list()
    for h in OPS[3]['header']:
        if h in dj:
            row.append(dj[h])
        else:
            row.append('')
            raise ReferenceError(f'Op 04: Invalid key "{h}"')
    # c.writerow(row)
    return row


################################################################################
def get_category_05(accesskey, secretkey, category_code):
    # c.writerow(OPS[4]['header'])
    _datetime = datetime.datetime.utcnow().strftime('%y%m%dT%H%M%SZ')
    method = "GET"
    path = f'/v2/providers/seller_api/apis/api/v1/marketplace/meta/display-categories/{category_code}'
    message = _datetime + method + path
    url = "https://api-gateway.coupang.com" + path
    signature = hmac.new(secretkey.encode('utf-8'), message.encode('utf-8'),
                         hashlib.sha256).hexdigest()
    authorization = "CEA algorithm=HmacSHA256, access-key=" + accesskey + \
                    ", signed-date=" + _datetime + ", signature=" + signature
    headers = {
        'Content-type': 'application/json;charset=UTF-8',
        'Authorization': authorization,
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code // 10 != 20:
        sys.stderr.write(resp.text)
        raise LookupError(f"get_product_02: Invalid API response code {resp.status_code}")
    # print(resp.text)
    rj = json.loads(resp.text)
    dj = rj['data']
    # pprint(dj)
    row = list()
    for h in OPS[4]['header']:
        if h in dj:
            row.append(dj[h])
        else:
            row.append('')
            raise ReferenceError(f'Op 05: Invalid key "{h}"')
    # c.writerow(row)
    return row


################################################################################
def get_safe_row(row):
    for i in range(len(row)):
        if row[i] is None:
            row[i] = ''
        elif isinstance(row[i], str):
            # escape sequence for mysql
            if row[i].find("'") >= 0:
                row[i] = str(row[i]).replace("'", "''")
            if row[i].find("'") >= 0:
                row[i] = str(row[i]).replace("\\", "\\\\")
            if row[i].find("&nbsp;") >= 0:
                row[i] = str(row[i]).replace("&nbsp;", " ")
            if row[i].find("&quot;") >= 0:
                row[i] = str(row[i]).replace("&quot;", '"')
            if row[i].find("&apos;") >= 0:
                row[i] = str(row[i]).replace("&apos;", "''")
            if row[i].find("&amp;") >= 0:
                row[i] = str(row[i]).replace("&amp;", "&")
            if row[i].find("&lt;") >= 0:
                row[i] = str(row[i]).replace("&lt;", "<")
            if row[i].find("&gt;") >= 0:
                row[i] = str(row[i]).replace("&gt;", ">")
        elif isinstance(row[i], (list, tuple)):
            row[i] = ','.join(map(str, row[i]))
        else:
            row[i] = str(row[i])
    return row


################################################################################
def upsert_01_02(logger, rows, sio, shop_id):
    sio.write('\n--- 상품목록 페이징조회 + 상품조회\n')
    for row in rows:
        try:
            if len(row) != 37:
                raise RuntimeError(f'상품목록 페이징조회 + 상품조회 #columns must 37 but {len(row)}')
            row.insert(0, shop_id)
            row = get_safe_row(row)
            sio.write("REPLACE INTO CBCI_COUPANG_GOODS VALUES ('{0}',NOW());\n".format(
                "','".join(row)
            ))
        except Exception as e:
            msg = 'upsert_01_02 Error: %s' % str(e)
            logger.error(msg)


################################################################################
def b64_encode(row, ndxs):
    for ndx in ndxs:
        s = row[ndx]
        if not s:
            continue
        row[ndx] = base64.b64encode(s.encode("utf-8")).decode("utf-8")


################################################################################
def get_valid_text_desc(row, ndxs):
    for ndx in ndxs:
        s = str(row[ndx])
        if s.lower() not in ('text', 'text_text', 'title'):
            row[ndx+1] = ''
            row[ndx+2] = ''


################################################################################
def upsert_03_04(logger, rows, sio, shop_id):
    sio.write('\n--- 재고관리 상품조회 + 상품 아이템별 수량/가격/상태 조회\n')
    for row in rows:
        try:
            if len(row) != 109:
                raise RuntimeError(f'재고관리 상품조회 + 상품 아이템별 수량/가격/상태 조회 '
                                   f'#columns must 109 but {len(row)}')
            sql = SQL_CBCI_COUPANG_STOCK
            # b64_encode(row, [91, 94, 97, 100, 103])
            get_valid_text_desc(row, [90, 93, 96, 99, 102])
            row = get_safe_row(row)
            sql = sql.replace('SHOP_ID', shop_id)
            sql_out = sql.format(*row)
            sio.write(sql_out)
            sio.write('\n')
        except Exception as e:
            msg = 'upsert_03_04 Error: %s' % str(e)
            logger.error(msg)


################################################################################
def upsert_05(logger, rows, sio):
    sio.write('\n--- 카테고리 조회\n')
    for row in rows:
        try:
            if len(row) != 4:
                raise RuntimeError(f'카테고리 조회 #columns must 4 but {len(row)}')
            row = get_safe_row(row)
            sio.write("REPLACE INTO CBCI_COUPANG_CATEGORY VALUES ('{0}');\n".format(
                "','".join(row)
            ))
        except Exception as e:
            msg = 'upsert_05 Error: %s' % str(e)
            logger.error(msg)


################################################################################
def do_api(mcxt, args):
    try:
        mcxt.logger.info('>>>starting...')
        if not args.accesskey:
            raise ValueError(f'Invalid "Access key"="{args.accesskey}"')
        if not args.secretkey:
            raise ValueError(f'Invalid "Secret key"="{args.secretkey}"')
        if not args.vendor_id:
            raise ValueError('"Vendor Id" must be provided')

        sio = StringIO()
        sio.write(f'--- 쿠팡 API 조회 결과 Vendor Id = "{args.vendor_id}"\n')

        seller_product_ids = list()
        display_category_codes = list()

        # 1) 01, 02 API
        rows_01 = seller_products_01(args.accesskey, args.secretkey, args.vendor_id,
                                     sio, seller_product_ids, display_category_codes)
        for i, seller_product_id in enumerate(seller_product_ids):
            try:
                row_02 = get_product_02(args.accesskey, args.secretkey, seller_product_id)
                rows_01[i].extend(row_02)
            except Exception as e:
                msg = '01, 02 Loop Error: %s' % str(e)
                mcxt.logger.error(msg)

        upsert_01_02(mcxt.logger, rows_01, sio, args.shop_id)

        # 2) 03, 04 API
        for i, seller_product_id in enumerate(seller_product_ids):
            try:
                vendor_item_ids = list()
                rows_03 = get_product_03(args.accesskey, args.secretkey, seller_product_id,
                                         vendor_item_ids)
                for j, vendor_item_id in enumerate(vendor_item_ids):
                    try:
                        row_04 = get_inventories_04(args.accesskey, args.secretkey, vendor_item_id)
                        rows_03[j].extend(row_04)
                    except Exception as e:
                        msg = '03, 04 Loop Detail Error: %s' % str(e)
                        mcxt.logger.error(msg)
                upsert_03_04(mcxt.logger, rows_03, sio, args.shop_id)
            except Exception as e:
                msg = '03, 04 Loop Error: %s' % str(e)
                mcxt.logger.error(msg)

        # 3) 05 API
        rows_05 = list()
        for display_category_code in display_category_codes:
            try:
                row_05 = get_category_05(args.accesskey, args.secretkey, display_category_code)
                rows_05.append(row_05)
            except Exception as e:
                msg = '05 Loop Error: %s' % str(e)
                mcxt.logger.error(msg)
        upsert_05(mcxt.logger, rows_05, sio)
        print(sio.getvalue(), end='')
        return 0
    except Exception as e:
        msg = 'argoslabs.shop.coupang Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
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
        display_name='Coupang API',
        icon_path=get_icon_path(__file__),
        description='Coupang Shopping API',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('accesskey',
                          display_name='Access key',
                          input_method='password',
                          help='Access key for Coupang API')
        mcxt.add_argument('secretkey',
                          display_name='Secret key',
                          input_method='password',
                          help='Secret key for Coupang API')
        mcxt.add_argument('vendor_id',
                          display_name='Vendor Id',
                          help='Vendor Id for Coupang API')
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
