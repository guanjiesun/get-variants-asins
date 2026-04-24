"""
根据 ASIN 详情页获取所有变体的 ASIN 信息
"""
import httpx
from lxml import html

import json
import random
import time

class ASINExtractor:
    pass

def get_price(url: httpx.URL) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0"}
    r = httpx.get(url, headers=headers)
    tree = html.fromstring(r.text)
    results = tree.xpath("//*[@id='centerCol']//span[contains(@class, 'apex-pricetopay-value')]")
    if results:
        result = results[0]
        return result.text_content().strip()
    else:
        return 'NotFound'

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
                info['ASIN'] = asin.strip()
                info['Color'] = color_size[0].strip()
                info['Size'] = color_size[1].strip()
                info['Price'] = get_price(url)
                info['URL'] = str(url)
                print(f'{info["ASIN"]}, {info["Color"]}, {info["Size"]}, {info["Price"]}, {info["URL"]}')
                result.append(info)
                time.sleep(random.randint(30, 60))

    return result
