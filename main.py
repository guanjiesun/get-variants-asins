import json
import asyncio

import zendriver

def get_target_dict(html_content):
    # This regex is robust and correct for extracting the JSON
    key_name = "dimensionValuesDisplayData"
    lines = html_content.splitlines()
    for line in lines:
        if key_name in line:
            line = line.strip()
            key, value = line.split(':', 1)
            value = value.strip(' ,')
            d = json.loads(value)
            cnt = 0
            for k, v in d.items():
                print(f'{cnt+1}-{k}: {v}')
                cnt += 1

async def main():
    asin = 'B0BLYSGFRW'
    url = f'https://www.amazon.com/dp/{asin}'

    browser = await zendriver.start()

    # 获取主标签页
    tab = await browser.get(url)
    await tab.maximize()
    await tab.wait_for_ready_state(until='complete', timeout=120)
    content = await tab.get_content()
    get_target_dict(content)
    await asyncio.sleep(3)
    await browser.stop()

if __name__ == '__main__':
    asyncio.run(main())
