import httpx
from lxml import html

import re
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

def main():
    url = httpx.URL('https://www.amazon.com/dp/B0D499LWSN')

    try:
        price: Price = get_price(url)
        print(price)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
