"""
根据 ASIN 详情页获取所有变体的 ASIN 信息
"""

import json

def get_asins(html: str) -> list[dict]:
    """解析网页内容以获取所有 asin 信息"""
    result = list()
    key_name = "dimensionValuesDisplayData"
    lines = html.splitlines()
    for line in lines:
        if key_name in line:
            line = line.strip()
            key, value = line.split(':', 1)
            value = value.strip(' ,')
            d = json.loads(value)

            for asin, color_size in d.items():
                info = dict()
                info['ASIN'] = asin.strip()
                info['COLOR'] = color_size[0].strip()
                info['SIZE'] = color_size[1].strip()
                result.append(info)
    return result
