"""
根据 ASIN 详情页获取所有变体的 ASIN 信息
"""
import httpx
from lxml import html

import json
import random
import re
import time
from collections import namedtuple

Price = namedtuple('Price', ['pay_price', 'typical_price', 'list_price', 'coupon_price'])

def get_price(url: httpx.URL) -> Price:
    """
    给定一个 asin 的 url，返回获取到的 4 个价格信息
    :param url: 如'https://www.amazon.com/dp/B0DGL6Q56X'
    :return: 包含 4 个价格信息的容器
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0"}
    r = httpx.get(url, headers=headers)
    tree = html.fromstring(r.text)

    # 获取 pay_price
    elements = tree.xpath("//*[@id='centerCol']//span[contains(@class, 'apex-pricetopay-value')]")
    if elements:
        pay_price = elements[0].text_content().strip()
        pay_price = float(pay_price.split('$')[-1])
    else:
        pay_price = 'NotFound'

    # 获取 typical_price or list_price
    elements = tree.xpath("//*[@id='centerCol']//span[contains(@class, 'apex-basisprice-value')]/span[position()=1]")
    if elements:
        typical_list_ele = elements[0]
        parent_text = typical_list_ele.getparent().getparent().text.strip().lower()
        if 'list price' in parent_text:
            typical_price = 'NotFound'
            list_price = typical_list_ele.text.strip()
            list_price = float(list_price.split('$')[-1])
        else:
            list_price = 'NotFound'
            typical_price = typical_list_ele.text.strip()
            typical_price = float(typical_price.split('$')[-1])
    else:
        typical_price, list_price = 'NotFound', 'NotFound'

    # 获取 coupon_price
    elements = tree.xpath("//*[contains(@id, 'couponText')]")
    if elements:
        coupon_price_ele = elements[0]
        digits = re.findall(r'\d+', coupon_price_ele.text)
        if digits:
            coupon_discount = int(digits[0])
            coupon_price = pay_price * (1 - coupon_discount / 100)
        else:
            coupon_price = 'NotFound'
    else:
        coupon_price = 'NotFound'

    return Price(pay_price, typical_price, list_price, coupon_price)

def get_asins(html_content: str) -> list[dict]:
    """解析网页内容以获取所有 asin 信息"""
    result = list()
    key_name = "dimensionValuesDisplayData"
    lines = html_content.splitlines()
    for line in lines:
        if key_name in line:
            line = line.strip()
            key, value = line.split(':', 1)
            value = value.strip(' ,')
            d = json.loads(value)

            for asin, color_size in d.items():
                info = dict()
                url = httpx.URL(f'https://www.amazon.com/dp/{asin}')

                # 获取 ASIN, Color and Size 信息
                info['ASIN'] = asin.strip()
                info['Color'] = color_size[0].strip()
                info['Size'] = color_size[1].strip()

                # 获取价格信息
                pay_price, typical_price, list_price, coupon_price = get_price(url)
                info['PayPrice'] = pay_price
                info['TypicalPrice'] = typical_price
                info['ListPrice'] = list_price
                info['CouponPrice'] = coupon_price

                # 添加 ASIN 的 URL
                info['URL'] = str(url)
                print(info)
                result.append(info)
                time.sleep(random.randint(30, 60))

    return result
