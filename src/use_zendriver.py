import json
import asyncio

import zendriver
import pandas as pd

def get_mappings(html_content) -> list[dict]:
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
                info['ASIN'] = asin.strip()
                info['COLOR'] = color_size[0].strip()
                info['SIZE'] = color_size[1].strip()
                result.append(info)
    return result

async def main():
    asin = 'B0BLYSGFRW'
    url = f'https://www.amazon.com/dp/{asin}'

    browser = await zendriver.start()

    # 获取主标签页
    tab = await browser.get(url)
    await tab.maximize()
    await tab.wait_for_ready_state(until='complete', timeout=120)

    # 获取网页源码
    html_content = await tab.get_content()

    # 从网页源码中找到所有变体的信息（asin-size-color）
    result = get_mappings(html_content)

    # 将结果写入 excel 文件
    df = pd.DataFrame(result)
    df.to_excel(f'{asin}.xlsx', index=False, engine='openpyxl')

    # 关闭浏览器
    await asyncio.sleep(3)
    await browser.stop()

if __name__ == '__main__':
    asyncio.run(main())
