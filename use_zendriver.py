"""
根据 ASIN 详情页获取所有变体的 ASIN 信息
工具: zendriver
"""

import asyncio
from pathlib import Path

import zendriver
import pandas as pd

from .get_asins import get_asins

async def get_asins_by_zendriver(asin: str, dst_folder: Path) -> None:
    # 设置输入参数
    url: str = f'https://www.amazon.com/dp/{asin}'
    dst_file: Path = dst_folder / f'{asin}-zendriver.xlsx'

    # 启动浏览器
    browser = await zendriver.start()

    # 打开 asin 对应的详情页
    tab = await browser.get(url)
    await tab.maximize()
    await tab.wait_for_ready_state(until='complete', timeout=120)

    # 获取网页源码
    html_content = await tab.get_content()

    # 从网页源码中找到所有变体的信息（asin-size-color）
    result = get_asins(html_content)

    # 将结果写入 excel 文件
    df = pd.DataFrame(result)
    df.to_excel(dst_file, index=False, engine='openpyxl')

    # 关闭浏览器
    await asyncio.sleep(3)
    await browser.stop()

if __name__ == '__main__':
    asyncio.run(get_asins_by_zendriver(asin='B0BLYSGFRW', dst_folder=Path().cwd()))
