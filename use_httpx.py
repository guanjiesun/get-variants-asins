"""
根据 ASIN 详情页获取所有变体的 ASIN 信息
工具: httpx
"""

import asyncio
from pathlib import Path

import httpx
import pandas as pd

from .get_asins import get_asins

async def get_asins_by_httpx(asin: str, dst_folder: Path) -> None:
    # 设置输入参数
    url: str = f'https://www.amazon.com/dp/{asin}'
    dst_file: Path = dst_folder / f'{asin}-httpx.xlsx'

    # 构造请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0"}

    # 发起 GET 请求
    async with httpx.AsyncClient(headers=headers) as client:
        r = await client.get(url)

        # 从网页源码中找到所有变体的信息（asin-size-color）
        result = get_asins(r.text)

        # 将结果写入 excel 文件
        df = pd.DataFrame(result)
        df.to_excel(dst_file, index=False, engine='openpyxl')

if __name__ == '__main__':
    asyncio.run(get_asins_by_httpx(asin='B0BLYSGFRW', dst_folder=Path().cwd()))
